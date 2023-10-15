# Insurance Cross Sell Project 🚙

![](imgs/vehicle_insurance.jpeg)

# 1.0 Business Problem
    
Health Insurance is a fictitious company that has been offering health insurance services to its customers for over 10 years across the world. Seeking to expand its spectrum of activity, the company now wishes to offer its customer base vehicle insurance.

To this end, a survey was carried out with approximately 304 thousand customers in order to understand which ones were interested or not in purchasing the new insurance. This data was then stored in a database and now the company has a base of 76 thousand new customers to whom it wants to offer the new insurance.
  
The plan is to allocate part of the sales team to contact these customers via **telephone** offering insurance. Given the number of salespeople and the budget allocated to the project, the team has the capacity to make up to 20 thousand calls to the potential customer base.

With this project restriction, Health Insurance would like to reach as many people interested in insurance as possible within the limit of possible calls.
  
To do this, it hired a team of data scientists so that they could select the best customers from the potential base for offering insurance and and store the customer data in a table in Google Sheets.

# 2.0 Business Assumptions

- The sales team already uses Google Sheets as a corporate tool. The purchasing propensity ranking needs to be incorporated into it.

## 2.1 Data Description

| Store              | Sales      
| ------------------ | ---------- 
|id	                 | Unique identifier for each customer
|Gender | Customer gender
|Driving_License | 0 : Customer does not have a driver's license, 1 : Customer has a driver's license
|Region_Code | Unique region identifier
|Vehicle_Insured | 1 : Customer already has vehicle insurance, 0 : Customer does not have vehicle insurance
|Vehicle_Age | Vehicle age
|Vehicle_Damage | 1: Customer has had his car damaged before. 0: Customer has never had their car damaged
|Annual_Premium | Amount to be paid annually to take out the insurance
|Sales_Channel | Identifier of the channel in which the research was carried out (email, telephone, etc.)
|Days_Client_Associate | Total number of days that the customer is associated with the company
|Interested | 1 : Customer is interested in vehicle insurance, 0 : Customer is not interested

# 3.0 Solution Strategy

Based on the interest survey carried out by the company regarding the new insurance, which gathered various data from potential customers, the model proposed in this project will be able to **calculate the probability (score) of a given individual taking out insurance or not* *.

For example, between a customer A with a 20% probability of signing up for insurance and another customer B with a 70% probability, the **sales team should choose to contact customer B** first. With the probability of insurance adherence calculated for all customers in the potential base, it is possible to order the list by probability, from highest to lowest, and activate the clients with the highest probability first, thus increasing the conversion of the operation.

The following image seeks to illustrate this process:
 
![](imgs/system_img.png)

In an overview, the solution process for this problem was elaborated as follows

1. First, the data from the interest survey carried out by the company was divided into two parts, one with 80% of the data and the other with 20%. This data was used to train and evaluate the algorithm in a cross validation process, training the algorithm with the largest portion and evaluating its metrics with the smallest.
2. After this evaluation, the algorithm to be used in the project was chosen
3. With the model chosen and the hyperparameters adjusted, the new customer base is applied to the model to obtain probabilities and order the list for the sales team
4. Assuming that the bases are homogeneous, we can generalize the metrics obtained in validating the model to the new customer base, thus measuring the performance of the operation with this new base

This process can be illustrated by the following image:

![](imgs/system_img.png)

# 4.0 Some Insights

Foi realizada uma análise exploratória dos dados a fim de entender alguns de seus comportamentos e distribuições. Neste processo, alguns insights foram gerados, o 3 principais foram:

## 1) Older people tend to be more interested in purchasing car insurance.

- **True** 

![](imgs/boxplot.png)

## 2) People with new vehicles (< 1 year old) tend not to be interested in purchasing car insurance.

- **True** 

![](imgs/vehicle_age.png)

## 3) It is possible to say that people who already have insurance are not interested in purchasing car insurance.

- **True** 

![](imgs/vehicle_insured.png)

## 4) It is possible to say that people who have never had their car damaged are not interested in purchasing car insurance.

- **True** 

![](imgs/vehicle_damage.png)

# 5.0 Machine Learning

To define the best model to be used, 5 different classification models were tested. These were evaluated mainly by ranking metrics (a key point in this project) but also by the ranking metrics themselves.

The main metrics observed were:

- Precision at K
- Recall at K

The Classification metrics were also observed:

- Accuracy
- Precision
- Recall
- F1 Score

To evaluate the metrics of all tested models in a more reliable way, the Cross Validation technique was used

In this process, the model is trained and validated with different segments of the available dataset in order to reduce any bias that may occur during the separation of data for training. This operation can be illustrated below:

![](imgs/gain_curve.png)
  
The ranking metrics for all tested models are shown below:

| Model                | Precision at K      | Recall at K     
| -------------------- | ------------------- | --------------------
| KNN                  | 0.2188 +/- 0.0009   | 0.9370 +/- 0.0039
| Logistic Regression  | 0.2320 +/- 0.0002   | 0.9935 +/- 0.0039
| Extra Trees          | 0.2286 +/- 0.0003   | 0.9792 +/- 0.0016
| XGBoost              | 0.2322 +/- 0.0002   | 0.9943 +/- 0.0010
| Light LGBM           | 0.2331 +/- 0.0002   | 0.9940 +/- 0.0011

Based on these metrics, the model chosen for this project was **XGBoost Classifier**

The adjustment of the hyperparameters of the chosen model was carried out using the Baysian Optimazation method.

In short, given an objective function (which in this work was the maximization of the model's accuracy) this method seeks the **global optimum** by approximating the real function of hyperparameters through a “false” function called a substitute function.

The advantage of this method is that it uses the results of previous iterations to decide future steps, changing or maintaining the strategy depending on the variation of the objective function at each iteration. A little more about this method can be found at [link](https://medium.com/analytics-vidhya/hyperparameter-search-bayesian-optimization-14be6fbb0e09).

For this application, the optuna library was used. The results of the method iterations until its convergence are shown below:

![](imgs/system_img.png)

# 6.0 Business Results

To measure the financial impacts of this project, an analysis was made from the perspective of the profit obtained from the operation comparing two approaches, the first without using the model and ordering customers and the second with the ordering given by the model.

This analysis was based on some premises:

- The profit obtained by the operation is equal to the revenue obtained from each converted customer subtracted from the customer acquisition cost
- Here we assume fictitious and fixed values ​​for revenue and customer acquisition costs as being 40 monetary units (u.m.) and 4 u.m. respectively.

The result of this analysis can be seen in the graph below:

![](imgs/bus_graph.png)

Infos:

![](imgs/bus_info.png)

# 7.0 Deployment in Render Cloud

For the business and sales team to access the model results, an API was built that returns the probability value (propensity score) of conversion of the customer of interest

Basically, based on the customer data provided by the user or application, the [Handler](http://Handler.py) file loads the necessary transformations to the data and the already trained model. Then, the prediction is made and this value is returned to the user.

The basic functioning of the API is demonstrated below:

![](imgs/system_img.png)

In order to facilitate the sales and business team's access to data, a [spreadsheet on Google Sheets](https://docs.google.com/spreadsheets/d/1wK0s_nfN0GdiEQOLKqZC0hthkC7nBdX-OX0s0r40mcw/edit#gid=0) was created that performs Predicting desired customers in a very simple way:

1. The data from the new customer base is inserted into the Google Sheets spreadsheet by the user
2. A button was created in the top menu called “propensity score” which, when clicked, generates the score of all customers entered in the spreadsheet
3. With the scores of all customers, the team will be able to start its operation

The following image show this spreadsheet:

![](imgs/gs.png)

# 8.0 Conclusions

# 9.0 Lessons Learned

# 10.0 Next Steps

As next steps and improvements for the evolution of this project, the following points were listed:

- Collection of new features that may be relevant for predicting customer conversion.
- Creation of new features based on existing features, which help in modeling the phenomenon.
- Facilitate access for the sales team to model predictions, improving the usability of the shared spreadsheet through buttons, instructions and feature selections
