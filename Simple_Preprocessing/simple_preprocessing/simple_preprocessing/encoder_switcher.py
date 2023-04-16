# Author: Marco Mungai Coppolino      
# License: BSD 3 clause      
      
import numpy as np      
import pandas as pd      
from operator import itemgetter      
      
from sklearn.preprocessing import OrdinalEncoder      
from sklearn.preprocessing import OneHotEncoder      
from sklearn.base import BaseEstimator, TransformerMixin      
      
      
class EncoderSwitcher(BaseEstimator, TransformerMixin):      
    """      
    Encode categorical features, allowing to decide on which features to      
    apply OneHotEncoding or OrdinalEncoding from scikit-learn.    
    The transformer will combine the output of the two encodings and sort   
    them keeping the original order of the columns of the input.      
      
    The input should be a numpy array or a pandas dataframe 
    The output can be a dataframe or a numpy array making the transformer     
    compatible and usable in Pipelines or Column Transformers.      
      
    There are two ways for the transformer to decide which encoder to perform
    on which features:      
        - The first way: deciding the max number of unique variables a      
           feature should have to be OneHot encoded.      
        - The second way: deciding the max total number of NEW columns that  
           should be created. The transformer will keep one-hot encoding
           features, starting from the one with the least amount of      
           variables, and proceeding in ascending order until the max total 
           number is reached.      
    The parameter check is used to decide what to do to the column that are
    not OneHot Encoded
    
    Parameters      
    ----------      
    max_num_columns : is the number that sets the limit of unique variables.  
        It must be a natural number. If it is set to 0 the transformer will  
        perform only ordinal encoding on the input dataframe.      
      
    total : a boolean keyword used to specify if max_num_columns is used      
        in the first way as a limit on how many unique variables a feature 
        can have to be one-hot encoded (total=False) or in the second way as  
        a limit on the total number of new columns the encoder will create 
        (total=True).      
      
    check : a boolean keyword, if True the transformer will perform a check  
        on the input dataframe/array and will encode only the categorical
        features (the ones with an "object" dtype) if False all the columns  
        will be encoded.      
      
    array : a boolean keyword, it is used to indicate if the output should
        be a pandas DataFrame (array=False), or a numpy array (array=True).  
        Keep it True if you are using the EncoderSwitcher in a PipeLine      
        or in a Column Transformer      
      
    Attributes      
    ----------      
    object_cols : a list containing the names of all the columns that will 
        be encoded. If the object in input is an array the names of those
        columns will be their location.       
        In this case, is important that both the fitted array and the       
        transformed one share the same column order or the encoder won't be  
        able to perform the right encoding. This is not a problem if the
        input is a dataframe because the name of the columns will be used as  
        a reference.      
      
    OHE_cols : a list containing the names of the columns that will be       
        one-hot encoded.      
      
    OE_cols : a list containing the names of the columns that  will be      
        ordinal encoded      
      
    fit_X_is_df : a boolean variable used in the functions of the transformer
        to keep track of the nature of the object in the input      
      
    num_cols_list : it's a particular list of lists of 2 elements that is
        used in the _switcher() function if total == True. (More detail on
        its purpose can be founded in that function)            
      
    """      
    def __init__(      
        self, max_num_columns=0, total=False, check=True, array=True      
    ):      
      
        self.max_num_columns = max_num_columns      
        self.total = total      
        self.check = check      
        self.array = array      
        self.object_cols = None      
        self.OHE_cols = None      
        self.OE_cols = None      
        self.fit_X_is_df = None      
        self.num_cols_list = None      
      
    def _check_keywords(self):      
        """      
        Perform a check on the input keywords.      
      
        """      
        if not isinstance(self.max_num_columns, int):      
            raise ValueError("max_num_columns is not a positive integer")     
 
        else:      
            if self.max_num_columns < 0:      
                raise ValueError("max_num_columns is not a positive integer") 

        if not isinstance(self.total, bool):      
            raise ValueError("total is not boolean")      
      
        if not isinstance(self.check, bool):      
            raise ValueError("check is not boolean")      
      
        if not isinstance(self.array, bool):      
            raise ValueError("array is not boolean")      
      
    def _check_input_X(self, X):      
        """      
        Perform a check on the input object to see if it is a dataframe or  
        an arry.      
      
        """      
        if isinstance(X, (pd.DataFrame, np.ndarray)):      
            return      
        else:       
            msg = (      
                "Object in input is not a pandas DataFrame or a numpy array"
            )      
            raise ValueError(msg)      
      
    def _switcher(self, X):      
        """      
        It's the function that fills OHE_cols and OE_cols, making a selection
        of which columns of the input dataframe/array, (named X), should be  
        one-hot encoded and which ones should be ordinal encoded.      
      
        """      
      
        # a conditional statement will define object_cols making a difference
        # based on the value of the keyword check.      
        if self.check:      
            self.object_cols = [      
                col for col in X.columns if X[col].dtype == "object"      
            ]      
        else:      
            self.object_cols = X.columns      
      
        # OHE_cols and OE_cols are resetted here to prevent problems in case
        # the encoder is fitted mistakenly multiple times.      
        self.OHE_cols = []      
        self.OE_cols = []      
      
        # the two decision method are now separated with a check on the      
        # total keyword      
        # First Method: total == False      
        if not self.total:      
            # the features with an equal or less amount of unique values than
            # max_num_columns are one-hot encoded the others are ordinal
            # encoded      
            for col in self.object_cols:      
                if X[col].nunique() <= self.max_num_columns:      
                    self.OHE_cols.append(col)      
                else:      
                    self.OE_cols.append(col)      
        # Second Method: total == True                  
        else:      
            # filling num_cols_list, a list in which every i-th element is   
            # a list of two things:      
            #   1. object_cols[i]      
            #   2. the number of unique values of the column associated with
            #       object_cols[i]      
            self.num_cols_list = [[      
                self.object_cols[0],      
                X[self.object_cols[0]].nunique()      
            ]]      
            for i in range(1, len(self.object_cols)):      
                self.num_cols_list.append([      
                    self.object_cols[i],      
                    X[self.object_cols[i]].nunique()      
                ])      
      
            # we will now sort num_cols_list in ascending order based on      
            # the number of unique elements      
            self.num_cols_list = sorted(     
                                     self.num_cols_list,      
                                     key=itemgetter(1)     
                                 )      
            # we will now select which column are OneHotEncoded      
            # and which one are OrdinalEncoded      
            num_columns = 0      
            for i in range(len(self.object_cols)):      
                if self.max_num_columns >= (num_columns +      
                                            self.num_cols_list[i][1] - 1):    

                    self.OHE_cols.append(self.num_cols_list[i][0])      
                    num_columns += self.num_cols_list[i][1] - 1       
                    # the -1 in the if condition and in the num_columns is 
                    # related to the fact that total should be the maximum 
                    # number of columns added to the original dataframe. 
                    # So, for this reason, we have to count the fact that 
  
                    # the columns made with the OHE take the place 
                    # of the columns of the orginal df. This means that, 
                    # for every new encoded feature i, we will have only: 
                    # self.num_cols_list[i][1] - 1 new columns        
                else:      
                    self.OE_cols.append(self.num_cols_list[i][0])      
      
        return self      
      
    def _sorter(self, X, OHE_X, OE_X):      
        """      
        It's the function responsible for the union of the two encoded 
        dataframe, OHE_X, and OE_X, with the not encoded columns of the 
        object in input. 
      
        Moreover, while concatenating the different parts this function 
        sorts the columns of the final dataframe (Encoded_X), making sure 
        that the original order of the features is preserved 
      
        """      
        # the function stars creating a list containing the names 
        # of the original columns of the dataframe.       
        X_cols_list = list(X.columns)      
      
        # we want to fill X_cols_list with the names of the new columns  
        # obtained after the OneHot Encoding.  
        # To understand how we are doing that it's important  
        # to keep in mind some things:  
        #   1. self.OHE_cols contains the names of the columns  
        #       of the dataset that are OneHot Encoded  
        #   2. self.OH_encoder.get_feature_names(self.OHE_cols) contains 
        #       the names of the columns after the OneHot Encoding 
        #   3. X[self.OHE_cols[i]].drop_duplicates().shape[0] will give us 
        #       the number of unique variables each OneHot Encoded feature 
        #       contains 
        # So using the names in self.OHE_cols we can find, in the database,  
        # the index of the encoded features and add the new columns in the 
        # rigth place. 
      
        k = 0      
        for i in range(len(self.OHE_cols)):      
            index = X_cols_list.index(self.OHE_cols[i])+1      
      
            for j in range(     
                         k,     
                         k + X[self.OHE_cols[i]].drop_duplicates().shape[0]
                     ):      
                X_cols_list.insert(     
                    index,      
                    self.OH_encoder.get_feature_names(self.OHE_cols)[j]     
                )      
                index += 1
                  
            k += X[self.OHE_cols[i]].drop_duplicates().shape[0]      
            X_cols_list.remove(self.OHE_cols[i])      
              
        # after X_cols_list is completed we concatenate, in a final      
        # dataframe, the two encoded datasets with the features       
        # not encoded, called Encoded_X      
        Encoded_X = pd.concat([      
            X[[col for col in X.columns if col not in self.object_cols]],
            OHE_X,      
            OE_X      
        ], axis=1)      
      
        # using X_cols_list we can easily sort Encoded_X in the right way     
 
        Encoded_X = Encoded_X[X_cols_list] 
        print(self.OH_encoder.get_feature_names(self.OHE_cols))
             
        if not self.array:      
            return Encoded_X      
        else:      
            return Encoded_X.values                   
      
    
    def fit(self, X, y=None):      
        """      
        Fit the EncoderSwitcher to X      
      
        """      
        # some checks on the input X and on the keywords of the encoder      
        self._check_input_X(X)      
        self._check_keywords()      
      
        # the switcher and the sorter are made to work with a dataframe      
        # thos is crucial especially to make the sorter work      
        # so we assure here that X is converted in a dataframe      
        if isinstance(X, np.ndarray):      
            self.fit_X_is_df = False      
            if self.check:      
                X = pd.DataFrame(X)      
                X = X.convert_dtypes(convert_string=False)      
            else:      
                X = pd.DataFrame(X)         
            X.columns = [str(col) for col in X.columns]      
        else:      
            self.fit_X_is_df = True      
      
        # the siwtcher fills OHE_cols and OE_cols      
        self._switcher(X)      
      
        # the two different encoders are then properly fitted       
        self.OH_encoder = OneHotEncoder(     
                              handle_unknown='ignore',      
                              sparse=False     
                          )      
        self.ordinal_encoder = OrdinalEncoder(      
                                   handle_unknown='use_encoded_value',      
                                   unknown_value=-999      
                               )      
        self.OH_encoder.fit(X[self.OHE_cols])      
        self.ordinal_encoder.fit(X[self.OE_cols])      
        return self      
      
    def transform(self, X):      
        """      
        Transform X using the EncoderSwitcher      
      
        """      
        self._check_input_X(X)      
      
        if isinstance(X, np.ndarray):      
            X = pd.DataFrame(X)      
            X.columns = [str(col) for col in X.columns]      
            X = X.convert_dtypes(convert_string=False)      
      
        OHE_X = pd.DataFrame(self.OH_encoder.transform(X[self.OHE_cols]))     
 
        OHE_X.index = X.index      
      
        OE_X = pd.DataFrame(self.ordinal_encoder.transform(X[self.OE_cols]))    
    
        OE_X.index = X.index      
      
        OHE_X.columns = self.OH_encoder.get_feature_names(self.OHE_cols)      
        OE_X.columns = self.OE_cols      
      
        Encoded_X = self._sorter(X, OHE_X, OE_X)      
        return Encoded_X       