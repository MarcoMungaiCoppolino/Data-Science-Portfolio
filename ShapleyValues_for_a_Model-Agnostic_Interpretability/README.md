# ShapleyValues_for_a_Model-Agnostic_Interpretability
The thesis "Shapley Values for a Model-Agnostic Interpretability" addresses how the increasing complexity of machine learning models in recent years has created the need for tools capable of explaining their predictions. In response to this need, the study presents an in-depth analysis of SHAP (SHapley Additive exPlanations), a collection of interpretability algorithms based on Shapley Values, a concept derived from Game Theory.

In particular, the thesis focuses on Model-Agnostic explanations—methods that can interpret the outcomes of any model rather than being tailored to a specific one. The text begins with an introduction outlining the importance of this approach and then introduces the theory behind Shapley Values through a simple game example.

Next, the focus temporarily shifts to analyzing a dataset containing samples of Portuguese “vinho verde” wine, associated with a classification problem. The goal is to predict the quality of wine samples based on physicochemical analysis results contained in the dataset. A Support Vector Machine (SVM) was chosen as the classifier, and the thesis includes the results of a hyperparameter optimization aimed at improving the algorithm’s accuracy.

After this digression, the discussion returns to SHAP, first demonstrating how the theoretical results can be adapted to Machine Learning models and then explaining the selected methods in detail. Finally, the last chapter presents the interpretation of the SVM, including an approach to handling feature correlation in the dataset—one of the most common challenges when using SHAP.
 
