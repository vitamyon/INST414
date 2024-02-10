import pandas as pd
df = pd.read_csv("listings.csv")
print(df.head())

unneeded_columns = ['id', 'name', 'host_id', 'host_name', 'latitude', 'longitude', 'minimum_nights', 'last_review', 'reviews_per_month', 'calculated_host_listings_count', 'availability_365', 'number_of_reviews_ltm', 'license']
df_cleaned = df.drop(columns=unneeded_columns)
print(df_cleaned.head())
df_cleaned_2 = df.dropna()
print(df_cleaned_2.head())

summary_stats = df.groupby(['neighbourhood_group', 'neighbourhood']).agg({
    'price': ['mean', 'median', 'min', 'max'],
    'number_of_reviews': ['mean', 'median', 'min', 'max']
})

grouped_data = df.groupby(['neighbourhood_group', 'neighbourhood'])
median_stats = grouped_data.agg({'price': 'median', 'number_of_reviews': 'median'})
top_price = median_stats.nlargest(10, 'price')
top_reviews = median_stats.nlargest(10, 'number_of_reviews')
print(top_price)
print(top_reviews)


neighborhood_popularity = df.groupby(['neighbourhood_group', 'neighbourhood']).size().reset_index(name='listings_count')
neighborhood_popularity_sorted = neighborhood_popularity.sort_values(by='listings_count', ascending=False)
print(neighborhood_popularity_sorted)


neighborhoods_of_interest = ['Hollywood', 'Long Beach', 'Venice', 'Beverly Hills', 'Santa Monica',
                             'Rancho Dominguez', 'Rolling Hills', 'East Compton', 'Elizabeth Lake', 'South Diamond Bar']
filtered_df = df[df['neighbourhood'].isin(neighborhoods_of_interest)]
avg_price_by_neighborhood = filtered_df.groupby('neighbourhood')['price'].mean().reset_index()
avg_price_by_neighborhood_sorted = avg_price_by_neighborhood.sort_values(by='price', ascending=False)
print(avg_price_by_neighborhood_sorted)