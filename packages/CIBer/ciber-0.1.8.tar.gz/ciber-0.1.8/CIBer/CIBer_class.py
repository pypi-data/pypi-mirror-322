import os, sys, scipy
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import warnings
from .CIBer_Engineering import Discretization, Joint_Encoding
import dill
copy_obj = lambda obj: dill.loads(dill.dumps(obj))

sys.path.append(os.path.dirname(scipy.stats.__file__))                          # read _stats.pyd
from _stats import _kendall_dis

class CIBer():
    def __init__(self, cont_col, asso_method='modified', min_asso=0.95, alpha=1, 
                 disc_method="norm", **kwargs):
        self.cont_col = cont_col
        if callable(asso_method):
            self.asso_method = asso_method
        else:
            self.asso_method = asso_method
        self.min_asso = min_asso
        self.alpha = alpha
        self.disc_method = disc_method
        self.discretizer = Discretization(cont_col, self.disc_method, **kwargs)
        self.encoder = Joint_Encoding()
        
        self.distance_matrix_ = dict()
        self.cluster_book = dict()
        if isinstance(asso_method, str): assert asso_method.lower() in ["spearman", "pearson", "kendall", "modified"]
        assert min_asso >= 0 and min_asso <= 1
        assert alpha > 0
        
        # Can be passed to sklearn.ensemble AdaBoostClassifier(estimator=CIBer(...))
        for key, value in kwargs.items():
            setattr(self, key, value)

        self._param_names = ['cont_col', 'asso_method', 'min_asso', 'alpha', 'disc_method'] + list(kwargs.keys())
    
    @staticmethod
    def _get_modified_tau(X_train):     # modified from scipy.stats._stats_py.kendalltau
        n_row, n_col = X_train.shape
        asso_matrix = np.diag(np.ones(n_col))
        tot = (n_row * (n_row - 1)) // 2
        two_unique = [len(np.unique(x)) > 2 for x in X_train.T]     # Not accept Binary as cm cluster
        
        for i in range(n_col - 1):
            if two_unique[i]:
                # sort on x and convert x to dense ranks
                x = X_train[:,i]
                perm = np.argsort(x)
                x = x[perm]
                x = np.r_[True, x[1:] != x[:-1]].cumsum(dtype=np.intp)
                for j in range(i+1, n_col):
                    if two_unique[j]:
                        y = X_train[perm,j]
                        # sort on y and convert y to dense ranks
                        perm2 = np.argsort(y)
                        sx, sy = x[perm2], y[perm2]
                        sy = np.r_[True, sy[1:] != sy[:-1]].cumsum(dtype=np.intp)
                        
                        dis = _kendall_dis(sy, sx)
                        tau = min(1., max(-1., (tot - 2*dis)/tot))
                        asso_matrix[i, j] = tau
                        asso_matrix[j, i] = tau
        
        return asso_matrix
        
    def _get_association(self, X_train):
        if isinstance(self.asso_method, str) and self.asso_method.lower() == "modified":
            asso_matrix = self._get_modified_tau(X_train)
        else:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)
                asso_matrix = pd.DataFrame(data=X_train).corr(method=self.asso_method).to_numpy()
        
        distance_matrix = np.nan_to_num(1 - np.absolute(asso_matrix), nan=1)
        AGNES = AgglomerativeClustering(metric='precomputed', linkage='complete', 
                                        distance_threshold=1-self.min_asso, n_clusters=None)
        AGNES.fit(distance_matrix)
        AGNES_clusters = AGNES.labels_
        return distance_matrix, sorted([np.where(AGNES_clusters == cluster)[0].tolist() for cluster in np.unique(AGNES_clusters)])
    
    def _get_prior_prob(self, y_train):
        # prior_prob: dict() key is class, value is the prior probability of this class
        classes, inverse = np.unique(y_train, return_inverse=True)      # return_inverse so that y_train can now take negative integers
        counts = np.bincount(inverse, weights=self.sample_weight)
        self.prior_prob = dict(zip(classes, counts/sum(counts)))
        self.y_cate = pd.Categorical(y_train, categories=classes)
    
    def fit(self, X_train, y_train, sample_weight=None):
        nrow, ncol = np.shape(X_train)
        self.sample_weight = np.ones(nrow) if sample_weight is None else nrow*sample_weight/sum(sample_weight)  # same weight on alpha
        assert len(self.sample_weight) == nrow
        
        self.cate_col = list(set(np.arange(ncol)) - set(self.cont_col))
        self.encoder.cate_col = self.cate_col
        
        if len(self.cont_col) > 0:
            X_train = self.discretizer.fit_transform(X_train, y_train)
        
        if len(self.cate_col) > 0:
            X_train = self.encoder.fit_transform(X_train)
        
        self.transform_X_train = X_train
        self.y_train = y_train
        # class_idx:  dict() key is class, value is a list containing the indices of instances for this class
        self.class_idx = {k: np.where(y_train == k)[0].tolist() for k in np.unique(y_train)}
        for c, idx in self.class_idx.items():
            self.distance_matrix_[c], self.cluster_book[c] = self._get_association(self.transform_X_train[idx,:])
        
        self.classes_ = np.array(list(self.class_idx.keys()))
        self.n_classes = len(self.classes_)
    
    def _get_cond_prob(self, X_train, X_test):
        ncol = np.shape(X_train)[1]
        self.cond_prob = dict()     # key is column, value dict: key is class, value is corresponding probabilities
        self.cond_cum_prob = dict() # key is column, value dict: key is class, value is corresponding cumulative probabilities
        self.prev_idx = dict()      # key is column, value dict: key is value, value is previous value
            
        for col in range(ncol):
            categories = np.unique(np.append(X_train[:,col], X_test[:,col]))
            x_cate = pd.Categorical(X_train[:,col], categories=categories)
            Laplace_tab = pd.crosstab(x_cate, self.y_cate, self.sample_weight, aggfunc="sum", dropna=False) + self.alpha
            density_tab = Laplace_tab.apply(lambda x: x/x.sum())
            
            if col in self.cont_col and self.disc_method == "ndd":
                density_tab = density_tab.rolling(window=3, min_periods=2, center=True).sum()
                density_tab = density_tab / density_tab.sum(axis=0)
                
            density_tab.loc[-1.0] = 0
            idx_lst = sorted(density_tab.index)
            density_tab = density_tab.reindex(index=idx_lst)
            self.cond_prob[col] = density_tab.to_dict()
            self.cond_cum_prob[col] = density_tab.cumsum().to_dict()
            self.prev_idx[col] = dict(zip(idx_lst[1:], idx_lst[:-1]))
        
    def predict_proba(self, X_test):
        if len(self.cont_col) > 0:
            X_test = self.discretizer.transform(X_test)
        
        if len(self.cate_col) > 0:
            X_test = self.encoder.transform(X_test)
        
        self.transform_X_test = X_test
        self._get_prior_prob(self.y_train)
        self._get_cond_prob(self.transform_X_train, self.transform_X_test)
        
        y_val = []
        for c in self.cluster_book.keys():
            indep_prob = {cluster[0]: self.cond_prob[cluster[0]][c] for cluster in self.cluster_book[c] if len(cluster) == 1}
            clust_prob = [{col: self.cond_cum_prob[col][c] for col in cluster} for cluster in self.cluster_book[c] if len(cluster) > 1]

            df_test = pd.DataFrame(X_test)
            prob = self.prior_prob[c] * df_test[indep_prob.keys()].replace(indep_prob).prod(axis=1)

            for comon_prob in clust_prob:
                prob_inf = df_test[comon_prob.keys()].replace(comon_prob).min(axis=1)
                prob_sup = df_test[comon_prob.keys()].replace(self.prev_idx).replace(comon_prob).max(axis=1)
                prob = prob * np.maximum(prob_inf - prob_sup, 1e-5)
            
            y_val.append(prob)
        
        # y_val is cond. likelihood, consider F_k is cond. log-llh F_{nk} = log(y_val_{nk}), then p_{nk} = y_val_{nk} / sum_k (y_val_{nk})
        return np.array(y_val).T / np.sum(y_val, axis=0).reshape(-1, 1)
    
    def predict(self, X_test):
        y_proba = self.predict_proba(X_test)
        return self.classes_[list(np.argmax(y_proba, axis=1))]
    
    def get_params(self, deep=True):
        return {param: getattr(self, param) for param in self._param_names}
    
    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

#%%
from scipy.optimize import minimize

class CAWCIBer(CIBer):
    def __init__(self, C=1.0, **kwargs):
        self.C = C
        super().__init__(**kwargs)
        
    def get_weighted_proba(self, omega_dict, X_train):
        y_val = []
        for c in self.cluster_book.keys():
            indep_prob = {cluster[0]: {key: value**w for key, value in self.cond_prob[cluster[0]][c].items()} for w, cluster in zip(omega_dict[c], self.cluster_book[c]) if len(cluster) == 1}
            clust_prob = [{col: self.cond_cum_prob[col][c] for col in cluster} for cluster in self.cluster_book[c] if len(cluster) > 1]
            clust_w    = [w for w, cluster in zip(omega_dict[c], self.cluster_book[c]) if len(cluster) > 1]

            df_test = pd.DataFrame(X_train)
            prob = self.prior_prob[c] * df_test[indep_prob.keys()].replace(indep_prob).prod(axis=1)

            for comon_prob, w in zip(clust_prob, clust_w):
                prob_inf = df_test[comon_prob.keys()].replace(comon_prob).min(axis=1)
                prob_sup = df_test[comon_prob.keys()].replace(self.prev_idx).replace(comon_prob).max(axis=1)
                prob = prob * np.maximum(prob_inf - prob_sup, 1e-5)**w
            
            y_val.append(prob)
        
        return np.array(y_val).T / np.sum(y_val, axis=0).reshape(-1, 1)
    
    def get_weight_dict(self, omega):
        length = np.cumsum([len(self.cluster_book[c]) for c in self.cluster_book.keys()])
        return dict(zip(self.cluster_book.keys(), np.split(omega, length)))
    
    def get_gradient(self, omega_dict, y_proba):
        y_hot_proba = np.eye(len(self.classes_))[self.y_train.reshape(-1)] - y_proba
        
        grad = np.array([])
        for col, c in enumerate(self.cluster_book.keys()):
            indep_prob = {cluster[0]: self.cond_prob[cluster[0]][c] for cluster in self.cluster_book[c] if len(cluster) == 1}
            clust_prob = [{col: self.cond_cum_prob[col][c] for col in cluster} for cluster in self.cluster_book[c] if len(cluster) > 1]
            clust_idx = [i for i, cluster in enumerate(self.cluster_book[c]) if len(cluster) > 1]
            
            df_test = pd.DataFrame(self.transform_X_train)
            df_indep = df_test[indep_prob.keys()].replace(indep_prob)
            for comon_prob, clust_col in zip(clust_prob, clust_idx):
                prob_inf = df_test[comon_prob.keys()].replace(comon_prob).min(axis=1)
                prob_sup = df_test[comon_prob.keys()].replace(self.prev_idx).replace(comon_prob).max(axis=1)
                col_name = "_".join(map(str, self.cluster_book[c][clust_col]))
                df_indep.insert(clust_col, col_name, np.maximum(prob_inf - prob_sup, 1e-5))
            
            grad = np.append(grad, -np.mean(y_hot_proba[:,col].reshape(-1, 1) * np.log(df_indep), axis=0).values + 2*self.gamma*(omega_dict[c] - 1))

        return grad
    
    def get_loss(self, omega):
        self.gamma = self.C * 1
        omega_dict = self.get_weight_dict(omega)
        y_proba = self.get_weighted_proba(omega_dict, self.transform_X_train)
        
        loss = -np.mean(np.log(y_proba[np.arange(len(y_proba)), self.y_train])) + self.gamma * np.sum((omega - 1)**2)
        grad = self.get_gradient(omega_dict, y_proba)
        return loss, grad
        
    def predict_proba(self, X_test):
        if len(self.cont_col) > 0:
            X_test = self.discretizer.transform(X_test)
        
        if len(self.cate_col) > 0:
            X_test = self.encoder.transform(X_test)
        
        self.transform_X_test = X_test
        self._get_prior_prob(self.y_train)
        self._get_cond_prob(self.transform_X_train, self.transform_X_test)
        
        omega = np.ones(sum(len(self.cluster_book[c]) for c in self.cluster_book.keys()))
        #omega = np.random.rand(sum(len(self.cluster_book[c]) for c in self.cluster_book.keys()))
        bds = ((0, 1) for _ in omega)
        res = minimize(self.get_loss, omega, method="L-BFGS-B", jac=True, bounds=bds)
        self.omega = self.get_weight_dict(res.x)
        #print(self.omega)
        return self.get_weighted_proba(self.omega, self.transform_X_test)
        
        

#%%
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score as CHIndex
from tqdm import tqdm, trange
             
def MAE(y_test, y_pred):
    return np.mean(np.abs(y_test - y_pred))

def MSE(y_test, y_pred):
    return np.mean((y_test - y_pred)**2)          

class KMeansRegressor():
    def __init__(self, clf, K_min=2, K_max=100, n_trials=5, seed=None, loss="mae", verbose=True):
        self.clf = clf
        self.K_max, self.n_trials, self.seed = int(K_max), int(n_trials), seed
        self.K_min = max(2, int(K_min))
        self.loss = loss
        self.verbose = verbose
        
        assert loss.lower() in ["mae", "mse"]
        self.loss_func = {'mae': MAE, 'mse': MSE}[loss.lower()]

    # Try KMeans() several times and output the best trial
    def _get_best_km(self, y_train, K):
        best_r, best_km = 0, None
        rng = np.random.RandomState(self.seed)
        for i in range(self.n_trials):
            km = KMeans(n_clusters=K, n_init="auto", random_state=rng).fit(y_train)
            r = CHIndex(y_train, km.labels_)
            if r > best_r:                                                  # update best_r if it is less than r
                best_r, best_km = r, km

        return best_km
    
    @staticmethod
    def _get_predict(X_test, clf, km):
        centers = km.cluster_centers_[np.unique(km.labels_)]                # remove centers that have no count; np.unique already sorted
        return (clf.predict_proba(X_test) @ centers).flatten()
        
    def fit(self, X_train, y_train, sample_weight=None):
        best_loss, best_clf, best_km, best_K = np.inf, None, None, None
        for K in (pbar := trange(self.K_min, self.K_max+1)) if self.verbose else range(self.K_min, self.K_max+1):
            km = self._get_best_km(y_train.reshape(-1, 1), K)
        
            clf = copy_obj(self.clf)
            clf.fit(X_train, km.labels_, sample_weight)
            y_pred = self._get_predict(X_train, clf, km)
            loss = self.loss_func(y_train, y_pred)
            
            _, cts = np.unique(km.labels_, return_counts=True)
            # avoid overfitting
            #if 1 - loss/best_loss > 1e-4 and min(cts) > max(len(y_train) * 1e-3, 50):
            if loss < best_loss:
                best_loss, best_clf, best_km, best_K = loss, clf, km, K
            
            if self.verbose:
                pbar.set_postfix_str(f"K={K}, {self.loss.upper()}={loss:.4}; " + 
                                     f"best K={best_K}, best {self.loss.upper()}={best_loss:.4}")
        
        self.best_clf, self.best_km = best_clf, best_km
    
    def predict(self, X_test):
        return self._get_predict(X_test, self.best_clf, self.best_km)
        

#%%
class AdaBoostCIBer(CIBer):
    def __init__(self, n_CIBer=5, verbose=True, **kwargs):
        self.n_CIBer = int(n_CIBer)
        self.verbose = verbose
        
        self.base_CIBer = CIBer(**kwargs)
        self.beta = np.ones(self.n_CIBer)
        
    def fit(self, X_train, y_train, sample_weight=None):
        self.base_CIBer.fit(X_train, y_train, sample_weight)
        self.classes_ = self.base_CIBer.classes_
        self.CIBer_lst = [copy_obj(self.base_CIBer) for i in range(self.n_CIBer)]
        
        sample_weight = self.base_CIBer.sample_weight
        K, nrow = len(self.classes_), len(y_train)
        for i, model in enumerate((pbar := tqdm(self.CIBer_lst)) if self.verbose else self.CIBer_lst) :
            model.sample_weight = sample_weight
            misclassify = y_train != model.predict(X_train)
            err = sum(misclassify*sample_weight)/sum(sample_weight)
            self.beta[i] = np.log((1 - err)/err) + np.log(K-1)
            sample_weight = sample_weight * np.exp(self.beta[i] * misclassify)  # SAMME
            sample_weight = nrow * sample_weight / sum(sample_weight)
            if self.verbose:
                pbar.set_postfix_str(f"misclassify={np.mean(misclassify):.4}")
        
    def predict_proba(self, X_test):
        y_val = 0
        for i, model in enumerate(self.CIBer_lst):
            y_val = y_val + self.beta[i] * model.predict_proba(X_test)
        
        return np.array(y_val) / np.sum(y_val, axis=1).reshape(-1, 1)
    
#%%
from joblib import Parallel, delayed

class GradientBoostClassifier():
    def __init__(self, reg, n_reg=100, seed=None, verbose=True):
        self.reg = reg
        self.n_reg = int(n_reg)
        self.rng = np.random.RandomState(seed)
        self.iter = trange(self.n_reg) if verbose else range(self.n_reg)
        
        self.gamma = np.zeros(self.n_reg)
        self.reg_lst = []
    
    @staticmethod
    def loss(y, p):                                                 # cross-entropy
        return -np.sum(y * np.log(p), axis=1)                       # l_n = sum_i (-y_{ni} ln p_{ni})
    
    @staticmethod
    def gradient(y, p):
        return p - y                                                # g_{ni} = p_{ni} - y_{ni}
    
    @staticmethod
    def hessian(y, p):
        h = - p[:,None,:] * p[:,:,None]                             # h_{nij} = - p_{ni} p_{nj}
        return h + np.einsum('ij,jk->ijk', p, np.eye(p.shape[1]))   # h_{nii} = p_{ni} (1 - p_{ni}) = p_{ni} - p_{ni} p_{ni}
    
    @staticmethod
    def softmax(val):
        exp_val = np.exp(val)
        return exp_val / exp_val.sum(axis=1).reshape(-1, 1)
    
    def _get_reg(self, X_train, y_train, sample_weight=None):
        _, n_col = X_train.shape
        
        def fit_reg(reg_k, k):
            reg_k.fit(X_train, y_train[:,k], sample_weight)
            return reg_k

        return list(Parallel(n_jobs=self.ncate, verbose=0)(
            delayed(fit_reg)(copy_obj(self.reg), k) for k in range(self.ncate)
        ))
    
    def fit(self, X_train, y_train, sample_weight=None):
        self.classes_, counts = np.unique(y_train, return_counts=True)
        y_lab = np.eye(len(self.classes_))[y_train.reshape(-1)]
        nrow, self.ncate = y_lab.shape
        
        y_val = np.ones(y_lab.shape) * np.log(counts / (nrow - counts)) + (2 * self.rng.rand(*y_lab.shape) - 1)
        h_val = np.zeros(y_lab.shape)
        for m in self.iter:
            y_prob = self.softmax(y_val)
            neg_grad = -self.gradient(y_lab, y_prob)
            '''
            reg_lst = self._get_reg(X_train, neg_grad, sample_weight)
            for k, reg_k in enumerate(reg_lst):
                h_val[:,k] = reg_k.predict(X_train)
            '''
            reg_lst = []
            for k in range(self.ncate):
                reg_k = copy_obj(self.reg)
                reg_k.fit(X_train, neg_grad[:,k], sample_weight)
                h_val[:,k] = reg_k.predict(X_train)
            
                reg_lst.append(reg_k)
            
            self.reg_lst.append(reg_lst)
            # gamma_m = sum_n (-g_n.T @ h_n) / sum_n (h_n.T @ H_n @ h_n)
            self.gamma[m] = np.sum(neg_grad * h_val) / np.sum(np.sum(h_val[:,:,None] * self.hessian(y_lab, y_prob), axis=1) * h_val)
            y_val = y_val + self.gamma[m] * h_val
    
    def predict_proba(self, X_test):
        y_val = np.zeros((len(X_test), self.ncate))
        for gamma, model_lst in zip(self.gamma, self.reg_lst):
            for k, reg_k in enumerate(model_lst):
                y_val[:,k] += gamma * reg_k.predict(X_test)
            
        return self.softmax(y_val)
    
    def predict(self, X_test):
        y_proba = self.predict_proba(X_test)
        return self.classes_[list(np.argmax(y_proba, axis=1))]