
# PriceRide

https://price-ride.vercel.app/

PriceRide is the most accurate on-road price estimator for motorcycles larger than 400cc in India. It achieves this by accurately calculating state-wise road taxes and CESS (if applicable) and predicting the initial 1+5 year insurance premium using a tuned XGB model based on comprehensive data collected for 80+ premium bikes sold in India, above 400ccs.

For the road tax and registration calculation, I utilized the GOI Parivahan's "Know Your MV Tax" website to accurately obtain state-wise road taxes and CESS (if applicable) and compiled them into a csv.

The training data for insurance prediction was compiled using the Motorcycles API and manually when required and includes every listed specification provided by the manufacturer. It additionally includes all current day exshowroom prices as of 30th March, 2025 and respective insurance premiums as provided to me by various dealers across India.


## Features

PriceRide is built on a 3-tier architecture with data for state-wise road tax and insurance prediction stored on Firebase, a FastAPI for calculating the on-road price connected to the front end hosted on Vercel.

The website's current functionality includes:

- A home page where users can automatically get the on-road prices of 80+ motorcycles across 10 different makes using dropdown menus.
  - The dropdowns adjust automatically for the selected make and send the power, torque and ex. showroom price figures from the dataset to the API.

- A custom calculation page for any motorcycles not included in the dataset or if ex. showroom prices of currently included motorcycles increase in the future, where other parameters can be chosen through dropdown menus as well.
  - Here the user specifies the make, ex. showroom, power and torque figures which are then sent to the API for price calculation.


## Screenshots

![Homepage](https://raw.githubusercontent.com/aaryant22/priceride-py/main/images/homepage.png)

![Results Page](https://raw.githubusercontent.com/aaryant22/priceride-py/main/images/resultscbu.png)

![Custom Page](https://raw.githubusercontent.com/aaryant22/priceride-py/main/images/customckd.png)

## How it Works

The hardest part of this project was coming up with an accurate means to predict insurance as rates seem to vary wildly from manufacturer to manufacturer. To investigate possible correlations, I started by compiling all specifications for every motorcycle whose price sheet I had access to. Once I had all the specifications, I attached the ex. showroom prices and insurance premiums given by dealers, I tried using multiple dealers across a few states to make this as accurate as possible.

Once I had all the data I needed, I set up a few correlation plots and 4 out 18 features seemed to affect insurance prices strongly : **make, ex. showroom price, power and torque**. So I figured it would be easiest to proceed with these 4 features as getting a user to input 4 features is much easier than getting them to input 18.

I tried several models and they yielded mixed results due to the nature of the data. The data is a mix of numeric and categorical data (often nominal) so preprocessing and accurate encoding was key. **XGBoost** with some clever tuning and feature engineering seemed to work best for lower and higher end motorcycles.

Now that we have the full context behind how insurance is predicted, the rest is fairly simple. Road tax is calculated state-wise depending on the type of motorcycle **(CBU/CKD/Locally Made)** . TCS is applicable on motorcycles whose ex. showroom price exceeds Rs. 10 lakh. Once we have everything we need its a simple summation. 

**Ex. showroom + Road Tax + TCS(if applicable) + Insurance (1+5 years) = On Road Price**
## Contributing

If you wish to contribute to PriceRide, have any improvements in mind, feel free to reach out! 

Some next steps include adding calculation for BH (Bharat Series) registration and adding a calculator for maintenance costs too.
