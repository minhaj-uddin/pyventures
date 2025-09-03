from tasks import process_data, fetch_data

# Trigger tasks asynchronously
process_data.apply_async(args=["sample_data"])
process_data.apply_async(args=["bad_data"])
fetch_data.apply_async()
