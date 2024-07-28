"""
Contains utils to parse and load experimental data
"""

from sklearn.model_selection import train_test_split

import pandas as pd
import re

import matplotlib.pyplot as plt

def load_amazon_data(data_dir, show_analysis=True):
    train_data = pd.read_csv(data_dir+'clothing_and_shoes_train.csv')
    test_data = pd.read_csv(data_dir+'clothing_and_shoes_test.csv')

    def convert_price_to_double(price_str):
        try:
            return float(re.sub(r'[^\d.]', '', price_str))
        except:
            return None

    def standardize_data(pdf):
        pdf = pdf\
            .rename(columns={'sub_category': 'category', 'name': 'product_title'})
        # fill null discount prices with actual prices
        pdf['price'] = pdf['discount_price'].fillna(pdf['actual_price']).apply(convert_price_to_double)

        return pdf[['product_title', 'main_category', 'category', 'price']]

    train_data, val_data = train_test_split(train_data, test_size=0.2, random_state=42)
    amazon_data = {'train': train_data, 'val': val_data, 'test': test_data}

    for key in amazon_data:
        raw_data = standardize_data(amazon_data[key]).sample(frac=1, random_state=42)
        raw_data['lm_prediction_targets'] = raw_data['product_title']
        amazon_data[key] = {
            'raw_data': raw_data
            }
        print (f'{key} has {len(raw_data)} samples')

    if show_analysis:
        # plot a grid of pie charts with 3 rows and 2 columns
        # rows are for training, validation and test data and columns are for main and sub categories
        fig, ax = plt.subplots(3, 2, figsize=(15, 15))

        for i, data in enumerate([b['raw_data'] for b in amazon_data.values()]):
            data['main_category'].value_counts().plot.pie(autopct='%.2f', ax=ax[i][0])
            data['category'].value_counts().plot.pie(autopct='%.2f', ax=ax[i][1])

        plt.show()

    return amazon_data

def load_flipkart_data(data_dir, show_analysis=True):
    train_data = pd.read_csv(data_dir+'clothing_and_footwear_train.csv')
    test_data = pd.read_csv(data_dir+'clothing_and_footwear_test.csv')

    train_data, val_data = train_test_split(train_data, test_size=0.2, random_state=42)

    def standardize_flipkart_data(pdf):
        pdf = pdf.copy()
        pdf['price'] = pdf['discounted_price'].fillna(pdf['retail_price'])

        generic_taglines = set([
            'Online in India. Shop Online For Apparels. Huge Collection of Branded Clothes Only at Flipkart.com',
            'from Flipkart.com. Only Genuine Products. 30 Day Replacement Guarantee. Free Shipping. Cash On Delivery!'
        ])

        def get_cleaned_description(row):
            desc = '' if row['description'] is None else str(row['description'])
            desc = desc.replace(row['product_name'], '')
            for tagline in generic_taglines:
                desc = desc.replace(tagline, '')
            desc = ' '.join(desc.split())
            return None if len(desc) < 50 else desc    
        
        pdf['description'] = pdf.apply(get_cleaned_description, axis=1)

        return pdf[['product_name', 'price', 'description', 'l1_category', 'l2_category', 'l3_category', 'product_specifications']]

    flipkart_data = {'train': train_data, 'val': val_data, 'test': test_data}

    for key in flipkart_data:
        raw_data = standardize_flipkart_data(flipkart_data[key]).sample(frac=1, random_state=42)
        raw_data['lm_prediction_targets'] = raw_data['product_name'] + ' ' + raw_data['description'].fillna('')
        flipkart_data[key] = {
            'raw_data': raw_data
        }
        num_non_empty_desc = len(raw_data[raw_data['description'].notnull()])
        print (f"Split: {key}, Number of products: {len(raw_data)}, Number of non-empty descriptions: {num_non_empty_desc}")

    if show_analysis:
        # plot a grid of pie charts with 3 rows and 3 columns
        # rows are for training, validation and test data and columns are for l1, l2, and l3 categories
        fig, ax = plt.subplots(3, 3, figsize=(15, 15))

        for i, data in enumerate([b['raw_data'] for b in flipkart_data.values()]):
            data['l1_category'].value_counts().plot.pie(autopct='%.2f', ax=ax[i][0])
            data['l2_category'].value_counts().plot.pie(autopct='%.2f', ax=ax[i][1])
            data['l3_category'].value_counts().plot.pie(autopct='%.2f', ax=ax[i][2])

        plt.tight_layout(); plt.show()
    
    return flipkart_data