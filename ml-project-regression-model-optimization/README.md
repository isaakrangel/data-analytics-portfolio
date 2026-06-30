# Regression Model Optimization Project

## Objective
Develop and compare multiple regression approaches to improve model performance through feature selection, scaling, and data transformations.

## Tools
- Python  
- Pandas  
- NumPy  
- Scikit-learn  
- Matplotlib / Seaborn  

## Process
- Data preprocessing and cleaning  
- Feature selection using correlation analysis  
- Feature scaling (Robust Scaler)  
- Feature transformation (Log1p)  
- Model training and comparison  
- Evaluation using R² and RMSE  

## Models Used
- Linear Regression  
- Ridge / Lasso Regression  
- Other regression models depending on experiments  
- Cross-validation for performance evaluation  

## Results
- Best performance achieved using correlation-based feature selection, no feature transformation, and Robust Scaler  
- Highest R²: 0.8995  
- Lowest RMSE: 1.7655  
- Log1p transformation reduced model performance  
- Model showed good predictions with no significant outliers  
- Consistent results across experiments indicate stable model behavior  

## Key Insights
- Feature selection had a major impact on model performance  
- Scaling improved stability and accuracy  
- Transformations (Log1p) did not improve results in this case  
- Model coefficients helped interpret feature influence and build the regression equation  
- Proper method selection is critical to avoid overfitting and underfitting  

## Skills Demonstrated
- Feature engineering  
- Regression modeling  
- Model evaluation (R², RMSE)  
- Feature selection techniques  
- Data scaling and transformation  
- Analytical thinking and experimentation
