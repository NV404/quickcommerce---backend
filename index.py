import json
import time
from flask import Flask, request, jsonify
import base64
import zlib
import subprocess
import shlex
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from flask_cors import CORS, cross_origin


def execute_curl_command2(curl_command):
    # Clean up the curl command to remove line continuations and join lines
    curl_command = ' '.join(
        line.strip('\\').strip() for line in curl_command.strip().splitlines()
    )
    # Parse the command into a list of arguments
    args = shlex.split(curl_command, posix=True)
    # Execute the curl command
    result = subprocess.run(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    # Check for errors
    if result.returncode != 0:
        return {'error': f'Error executing curl command: {result.stderr}'}
    else:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return {
                'error': 'Failed to parse JSON',
                'details': str(e),
                'output': result.stdout,
            }

def swiggy_search(query, latitude, longitude):
    curl_command_storeId = f"""
curl 'https://www.swiggy.com/api/instamart/home/select-location' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/json' \
  -H 'dnt: 1' \
  -H 'matcher: g9afg8eadfd87fecb9889df' \
  -H 'origin: https://www.swiggy.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.swiggy.com/instamart/' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  -H 'x-build-version: 2.246.0' \
  --data-raw '{{"data":{{"lat":{str(latitude)},"lng":{str(longitude)},"address":"11th Main Rd, HSR Layout, Sector 6, Bangalore, Karnataka 560102, India","addressId":"","annotation":"11th Main Rd, HSR Layout, Sector 6, Bangalore, Karnataka 560102, India","clientId":"INSTAMART-APP"}}}}'
    """

    response = execute_curl_command(curl_command_storeId)
    storeId = response['data']["storeId"]

    curl_command = f"""
    curl 'https://www.swiggy.com/api/instamart/search?pageNumber=0&searchResultsOffset=0&limit=40&query={query}&ageConsent=false&layoutId=3990&pageType=INSTAMART_SEARCH_PAGE&isPreSearchTag=false&highConfidencePageNo=0&lowConfidencePageNo=0&voiceSearchTrackingId=&storeId={storeId}&primaryStoreId={storeId}&secondaryStoreId={storeId}' 
      -H 'accept: */*' 
      -H 'accept-language: en-US,en;q=0.9' 
      -H 'content-type: application/json' 
      -H 'cookie: deviceId=s%3A44a8b5c3-29fd-4bd4-a815-7d4e94307ec2.92YIbkGgdfk%2FmoLjywylUh%2FLn%2FNpgYL0eQv9cckEDIE; versionCode=1200; platform=web; subplatform=dweb; statusBarHeight=0; bottomOffset=0; genieTrackOn=false; ally-on=false; isNative=false; strId=; openIMHP=false; webBottomBarHeight=0; _gcl_au=1.1.1701625907.1736853984; _ga=GA1.1.1273323290.1736853984; _fbp=fb.1.1736853983964.15207772092321315; tid=s%3A82f21c11-1ddf-45c9-882d-f613652abce0.NxIFQUfLX4Dxq2Irmfwh44M7XG3Fa0tJrWDN7jXfcOc; sid=s%3Aid661b2a-1c66-4c01-8ef4-87543db9ab0d.%2FgTLWUern%2Brk3Ia1KWkAcXLFVB%2FRLhQLgj%2FzT22CpM4; imOrderAttribution={{\\"entryId\\":null,\\"entryName\\":null,\\"entryContext\\":null,\\"hpos\\":null,\\"vpos\\":null,\\"utm_source\\":null,\\"utm_medium\\":null,\\"utm_campaign\\":null}}; _ga_8N8XRG907L=GS1.1.1736860928.2.1.1736860934.0.0.0' 
      -H 'dnt: 1' 
      -H 'matcher: 87ae98eadfd7gabe8e8aa99' 
      -H 'origin: https://www.swiggy.com' 
      -H 'priority: u=1, i' 
      -H 'referer: https://www.swiggy.com/instamart/search?custom_back=true&query={query}' 
      -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' 
      -H 'sec-ch-ua-mobile: ?0' 
      -H 'sec-ch-ua-platform: "macOS"' 
      -H 'sec-fetch-dest: empty' 
      -H 'sec-fetch-mode: cors' 
      -H 'sec-fetch-site: same-origin' 
      -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' 
      -H 'x-build-version: 2.246.0' 
      --data-raw '{{"facets":{{}},"sortAttribute":""}}'
    """

    # print(curl_command, "curl_command")

    data = execute_curl_command2(curl_command)

    return data

def execute_curl_command3(curl_command):
    import subprocess
    import json
    import gzip
    import io

    # Clean up the curl command
    curl_command = ' '.join(
        line.strip('\\').strip() for line in curl_command.strip().splitlines()
    )

    # Execute the curl command
    result = subprocess.run(
        curl_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    with gzip.GzipFile(fileobj=io.BytesIO(result.stdout)) as gzip_file:
        decoded_output = gzip_file.read().decode('utf-8')

            # For debugging: print the decoded output
        # print('Decoded Output (gzip):', decoded_output)
        return json.loads(decoded_output)

def zeptonow_search(query, latitude, longitude):
    curl_command_storeId = f"""
curl 'https://api.zeptonow.com/api/v1/config/layout/?latitude={str(latitude)}&longitude={str(longitude)}&page_type=HOME&version=v2&show_new_eta_banner=false&page_size=10' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'app_sub_platform: WEB' \
  -H 'app_version: 12.31.0' \
  -H 'appversion: 12.31.0' \
  -H 'compatible_components: CONVENIENCE_FEE,RAIN_FEE,EXTERNAL_COUPONS,STANDSTILL,BUNDLE,MULTI_SELLER_ENABLED,PIP_V1,ROLLUPS,SCHEDULED_DELIVERY,SAMPLING_ENABLED,ETA_NORMAL_WITH_149_DELIVERY,ETA_NORMAL_WITH_199_DELIVERY,HOMEPAGE_V2,NEW_ETA_BANNER,VERTICAL_FEED_PRODUCT_GRID,AUTOSUGGESTION_PAGE_ENABLED,AUTOSUGGESTION_PIP,AUTOSUGGESTION_AD_PIP,BOTTOM_NAV_FULL_ICON,COUPON_WIDGET_CART_REVAMP,DELIVERY_UPSELLING_WIDGET,MARKETPLACE_CATEGORY_GRID,PROMO_CASH:0,NEW_FEE_STRUCTURE,NEW_BILL_INFO,RE_PROMISE_ETA_ORDER_SCREEN_ENABLED,SUPERSTORE_V1,MANUALLY_APPLIED_DELIVERY_FEE_RECEIVABLE,MARKETPLACE_REPLACEMENT,ZEPTO_PASS,ZEPTO_PASS:1,ZEPTO_PASS:2,ZEPTO_PASS_RENEWAL,CART_REDESIGN_ENABLED,SUPERSTORE_V1,SHIPMENT_WIDGETIZATION_ENABLED,TABBED_CAROUSEL_V2,24X7_ENABLED_V1,PROMO_CASH:0,' \
  -H 'cookie: _gcl_au=1.1.334734093.1736966315; _ga=GA1.1.931613590.1736966315; _ga_52LKG2B3L1=GS1.1.1736966315.1.0.1736966315.60.0.356545521; _fbp=fb.1.1736966315261.329603733672865316' \
  -H 'device_id: 03c7cfde-70d5-4700-83a1-1867b68d39c3' \
  -H 'deviceid: 03c7cfde-70d5-4700-83a1-1867b68d39c3' \
  -H 'dnt: 1' \
  -H 'origin: https://lite.zeptonow.com' \
  -H 'platform: WEB' \
  -H 'priority: u=1, i' \
  -H 'referer: https://lite.zeptonow.com/' \
  -H 'request_id: 1ae24ac3-e16b-4e48-b130-e46a91b4f5b0' \
  -H 'requestid: 1ae24ac3-e16b-4e48-b130-e46a91b4f5b0' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'session_id: bbf957d4-02e5-4253-857a-8b05fac543fc' \
  -H 'sessionid: bbf957d4-02e5-4253-857a-8b05fac543fc' \
  -H 'store_etas: {{"fa5e892d-65d7-4da6-9bde-e1f22deb7b6f":-1}}' \
  -H 'store_id: fa5e892d-65d7-4da6-9bde-e1f22deb7b6f' \
  -H 'store_ids: fa5e892d-65d7-4da6-9bde-e1f22deb7b6f' \
  -H 'storeid: fa5e892d-65d7-4da6-9bde-e1f22deb7b6f' \
  -H 'tenant: ZEPTO' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  -H 'x-xsrf-token: gy6G9xxjq2hbtdnd5fB7i:OdW8byIew9Zzxco4UnrM3lcSROY.PDgQAyLqFY/QDbc7HO62bd1/UjdJpMsTXjq1s1U4tiU'
"""

    response = execute_curl_command3(curl_command_storeId)
    storeId = response["storeServiceableResponseV2"][0]["storeId"]

    # print(storeId, "storeId")

    # return storeId

    curl_command = f"""
curl 'https://api.zeptonow.com/api/v3/search' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'app_sub_platform: WEB' \
  -H 'app_version: 12.31.0' \
  -H 'appversion: 12.31.0' \
  -H 'compatible_components: CONVENIENCE_FEE,RAIN_FEE,EXTERNAL_COUPONS,STANDSTILL,BUNDLE,MULTI_SELLER_ENABLED,PIP_V1,ROLLUPS,SCHEDULED_DELIVERY,SAMPLING_ENABLED,ETA_NORMAL_WITH_149_DELIVERY,ETA_NORMAL_WITH_199_DELIVERY,HOMEPAGE_V2,NEW_ETA_BANNER,VERTICAL_FEED_PRODUCT_GRID,AUTOSUGGESTION_PAGE_ENABLED,AUTOSUGGESTION_PIP,AUTOSUGGESTION_AD_PIP,BOTTOM_NAV_FULL_ICON,COUPON_WIDGET_CART_REVAMP,DELIVERY_UPSELLING_WIDGET,MARKETPLACE_CATEGORY_GRID,PROMO_CASH:0,NEW_ROLLUPS_ENABLED,RERANKING_QCL_RELATED_PRODUCTS,PLP_ON_SEARCH,PAAN_BANNER_WIDGETIZED,ROLLUPS_UOM,DYNAMIC_FILTERS,PHARMA_ENABLED,AUTOSUGGESTION_RECIPE_PIP,SEARCH_FILTERS_V1,QUERY_DESCRIPTION_WIDGET,MEDS_WITH_SIMILAR_SALT_WIDGET,NEW_FEE_STRUCTURE,NEW_BILL_INFO,RE_PROMISE_ETA_ORDER_SCREEN_ENABLED,SUPERSTORE_V1,MANUALLY_APPLIED_DELIVERY_FEE_RECEIVABLE,MARKETPLACE_REPLACEMENT,ZEPTO_PASS,ZEPTO_PASS:1,ZEPTO_PASS:2,ZEPTO_PASS_RENEWAL,CART_REDESIGN_ENABLED,SUPERSTORE_V1,SHIPMENT_WIDGETIZATION_ENABLED,TABBED_CAROUSEL_V2,24X7_ENABLED_V1,PROMO_CASH:0,' \
  -H 'content-type: application/json' \
  -H 'cookie: _gcl_au=1.1.578867367.1736964025; _fbp=fb.1.1736964025071.281752712516196978; _ga=GA1.1.1269078819.1736964025; _ga_52LKG2B3L1=GS1.1.1736964025.1.0.1736964025.60.0.577284343' \
  -H 'device_id: 10fd5035-6465-4235-addf-58489f3f5c87' \
  -H 'deviceid: 10fd5035-6465-4235-addf-58489f3f5c87' \
  -H 'dnt: 1' \
  -H 'origin: https://lite.zeptonow.com' \
  -H 'platform: WEB' \
  -H 'priority: u=1, i' \
  -H 'referer: https://lite.zeptonow.com/' \
  -H 'request_id: 6f70a243-55a6-446a-8ac5-17c121aca3a8' \
  -H 'requestid: 6f70a243-55a6-446a-8ac5-17c121aca3a8' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'session_id: 35596b4d-a55e-486f-94ef-0d9a930d1557' \
  -H 'sessionid: 35596b4d-a55e-486f-94ef-0d9a930d1557' \
  -H 'store_etas: {{"{storeId}":8}}' \
  -H 'store_id: {storeId}' \
  -H 'store_ids: {storeId}' \
  -H 'storeid: {storeId}' \
  -H 'tenant: ZEPTO' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  -H 'x-without-bearer: true' \
  -H 'x-xsrf-token: bsd-K2t_GegoEq0GSkG-e:wY7CdG_yd57MXOZKMgWeMFDTUWM.BX8kBiTN4x2WQKhfVvG1Zg//PByXTp/6KjWvP+Ula94' \
  --data-raw '{{"query":"{query}","pageNumber":0,"intentId":"7aeb4e8b-6043-4d79-9acd-1883d3321dfd","mode":"AUTOSUGGEST"}}'
    """

    # print(curl_command, "curl_command")

    data = execute_curl_command3(curl_command)

    return data

def execute_curl_command(curl_command):
    import subprocess
    import json
    # Clean up the curl command to remove line continuations and join lines
    curl_command = ' '.join(line.strip('\\').strip() for line in curl_command.strip().splitlines())
    # Execute the curl command with shell=True
    result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    # Check for errors
    if result.returncode != 0:
        return {'error': f'Error executing curl command: {result.stderr}'}
    else:
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as e:
            return {'error': 'Failed to parse JSON', 'details': str(e), 'output': result.stdout}


def blinkit_search(query, latitude, longitude):
    # Replace placeholders in the curl command
    curl_command = f"""
    curl 'https://blinkit.com/v1/layout/search?q={query}&search_type=type_to_search' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'access_token: null' \
  -H 'app_client: consumer_web' \
  -H 'app_version: 1010101010' \
  -H 'auth_key: c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477' \
  -H 'content-type: application/json' \
  -H 'cookie: gr_1_deviceId=12d6ca04-8ddd-4a86-8269-7d4ac675b431; __cfruid=f9ba13d4a24261695e270f338a478e65ff486725-1736853572; _cfuvid=mp74EA8_4vH6wuuPY8jYAowguzAWMHZ7h9wK4GYUjVc-1736853572122-0.0.1.1-604800000; _gcl_au=1.1.1443572482.1736853572; _gid=GA1.2.910890585.1736853572; _fbp=fb.1.1736853572501.642880552105518762; gr_1_lat=12.9128455; gr_1_lon=77.63606999999999; gr_1_locality=3; city=Bangalore; gr_1_landmark=undefined; __cf_bm=psMLqTY5NOqw_BamTRCSNoNN23cdhnVOfKxe0K_h34U-1736860054-1.0.1.1-jDsL8We4j6Txny7EP0GJkQjBGWKj3Kam5G1x9JQAODSAo36FFsjc4TTvnLMJEeraau7f46dfor3T08TgYiMUTA; _gat_UA-85989319-1=1; _ga_DDJ0134H6Z=GS1.2.1736860054.2.1.1736860096.18.0.0; _ga=GA1.1.335642252.1736853572; _ga_JSMJG966C7=GS1.1.1736860054.2.1.1736860110.4.0.0' \
  -H 'device_id: 12d6ca04-8ddd-4a86-8269-7d4ac675b431' \
  -H 'dnt: 1' \
  -H 'lat: {str(latitude)}' \
  -H 'lon: {str(longitude)}' \
  -H 'origin: https://blinkit.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://blinkit.com/s/?q={query}' \
  -H 'rn_bundle_version: 1009003012' \
  -H 'sec-ch-ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'session_uuid: 16619e37-13b6-4a5f-b33f-f2fea141b5e9' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
  -H 'web_app_version: 1008010016' \
  --data-raw ''

    """

    response = execute_curl_command(curl_command)
    return response

def extract_products(json_data):
    # Initialize dictionaries to hold products from each website
    blinkit_products = {}
    swiggy_products = {}
    zeptonow_products = {}
    
    # Extract Blinkit products
    if 'blinkit' in json_data:
        blinkit_data = json_data['blinkit']
        # Assuming product data is under blinkit_data['response']['snippets']
        snippets = blinkit_data.get('response', {}).get('snippets', [])
        for snippet in snippets:
            # Check if the snippet contains product data
            if snippet.get('widget_type') == 'product_card':
                products = snippet.get('products', [])
                for product in products:
                    name = product.get('name', '')
                    image = product.get('image', '')
                    price = product.get('price', {}).get('mrp', 0)
                    blinkit_products[name] = {
                        'name': name,
                        'image': image,
                        'price': price
                    }
    
    # Extract Swiggy products
    if 'swiggy' in json_data:
        swiggy_data = json_data['swiggy']['data']
        widgets = swiggy_data.get('widgets', [])
        for widget in widgets:
            if widget.get('type') == 'PRODUCT_LIST':
                data = widget.get('data', {})
                items = data.get('data', [])
                if items and isinstance(items, list):
                    for item in items:
                        name = item.get('display_name', '')
                        variations = item.get('variations', [])
                        if variations:
                            variation = variations[0]  # Assuming first variation
                            images = variation.get('images', [])
                            image = images[0] if images else ''
                            price_info = variation.get('price', {})
                            price = price_info.get('offer_price', price_info.get('mrp', 0))
                            swiggy_products[name] = {
                                'name': name,
                                'image': image,
                                'price': price
                            }
    
    # Extract ZeptoNow products
    if 'zeptonow' in json_data:
        zeptonow_data = json_data['zeptonow']
        # Assuming products are under zeptonow_data['layout']
        layout = zeptonow_data.get('layout', [])
        for widget in layout:
            if widget.get('widgetName') == 'STORE_PRODUCTS_WIDGET':
                items = widget.get('data', {}).get('storeProducts', [])
                for product in items:
                    name = product.get('productName', '')
                    images = product.get('photos', [])
                    image = images[0] if images else ''
                    price = product.get('price', {}).get('finalPrice', 0)
                    zeptonow_products[name] = {
                        'name': name,
                        'image': image,
                        'price': price
                    }
    
    # Now, match products across websites
    combined_products = {}
    
    # Collect all product names
    all_product_names = set(blinkit_products.keys()) | set(swiggy_products.keys()) | set(zeptonow_products.keys())
    
    for name in all_product_names:
        combined_products[name] = {
            'name': name,
            'image': '',
            'prices': {}
        }
        # Blinkit
        if name in blinkit_products:
            combined_products[name]['image'] = blinkit_products[name]['image']
            combined_products[name]['prices']['blinkit'] = blinkit_products[name]['price']
        # Swiggy
        if name in swiggy_products:
            combined_products[name]['image'] = swiggy_products[name]['image']
            combined_products[name]['prices']['swiggy'] = swiggy_products[name]['price']
        # ZeptoNow
        if name in zeptonow_products:
            combined_products[name]['image'] = zeptonow_products[name]['image']
            combined_products[name]['prices']['zeptonow'] = zeptonow_products[name]['price']
    
    # Convert combined_products to a list
    result = list(combined_products.values())
    
    return result


def extract_blinkit_products(data):
    """Extract product details from Blinkit."""
    products = []
    if "blinkit" in data:
        for snippet in data["blinkit"].get("response", {}).get("snippets", []):
            cart_item = snippet.get("data", {}).get("atc_action", {}).get("add_to_cart", {}).get("cart_item", {})
            if cart_item:
                products.append({
                    "platform": "Blinkit",
                    "product_id": cart_item.get("product_id"),
                    "name": cart_item.get("product_name"),
                    "brand": cart_item.get("brand"),
                    "price": cart_item.get("price"),
                    "mrp": cart_item.get("mrp"),
                    "inventory": cart_item.get("inventory"),
                    "quantity": cart_item.get("quantity"),
                    "unit": cart_item.get("unit"),
                    "image_url": cart_item.get("image_url"),
                })
    return products

def extract_swiggy_products(data):
    """Extract product details from Swiggy."""
    products = []
    if "swiggy" in data:
        for widget in data["swiggy"].get("data", {}).get("widgets", []):
            for product in widget.get("data", []):
                for variation in product.get("variations", []):
                    products.append({
                        "platform": "Swiggy",
                        "product_id": variation.get("id"),
                        "name": variation.get("display_name"),
                        "brand": variation.get("brand"),
                        "price": variation.get("price", {}).get("offer_price"),
                        "mrp": variation.get("price", {}).get("mrp"),
                        "inventory": variation.get("inventory", {}).get("remaining"),
                        "quantity": variation.get("quantity"),
                        "unit": variation.get("sku_quantity_with_combo"),
                        "image_urls": variation.get("images", []),
                        "description": variation.get("meta", {}).get("long_description"),
                        "category": variation.get("category"),
                    })
    return products

def extract_zeptonow_products(data):
    """Extract product details from Zeptonow."""
    products = []
    if "zeptonow" in data:
        for layout in data.get("zeptonow", {}).get("layout", []):
            resolver_data = layout.get("data", {}).get("resolver", {}).get("data", {})
            items = resolver_data.get("items", [])
            if items and isinstance(items, list): 
                for item in items:
                    product_response = item.get("productResponse", {})
                    product_info = product_response.get("product", {})
                    product_variant = product_response.get("productVariant", {})
                    
                    price_info = product_response.get("price", {})
                    price = price_info.get("sp", 0) / 100
                    mrp = price_info.get("mrp", 0) / 100
                    images = product_variant.get("images", [])
                    image_urls = [img.get("path") for img in images if isinstance(img, dict)]
                    
                    products.append({
                        "platform": "Zeptonow",
                        "product_id": product_variant.get("id"),
                        "name": product_info.get("name", ""),
                        "brand": product_info.get("brand", ""),
                        "price": price,
                        "mrp": mrp,
                        "inventory": product_response.get("availableQuantity", 0),
                        "quantity": product_variant.get("quantity", 0),
                        "unit": product_variant.get("formattedPacksize", ""),
                        "image_urls": image_urls,
                        "description": " ".join(product_info.get("description", [])) if isinstance(product_info.get("description", []), list) else "",
                        "searchKeywords": product_info.get("searchKeywords", []),
                    })
            else:
                print(f"Unexpected 'items' structure in resolver data: {resolver_data}")
    return products


def parse_unit(unit):
    if not unit or not isinstance(unit, str):
        return None, None  # Return default values if unit is missing or invalid
    match = re.match(r"(\d+)\s*(\w+)(?:\s*x\s*(\d+))?", unit)
    if match:
        value = int(match.group(1))
        uom = match.group(2)
        multiplier = int(match.group(3)) if match.group(3) else 1
        return value * multiplier, uom
    return None, unit

# Normalize product information
def normalize_product(product):
    product["name"] = product["name"].lower()
    product["brand"] = product["brand"].lower()
    
    # Parse the unit safely
    total_quantity, uom = parse_unit(product.get("unit", ""))
    if total_quantity is None:
        print(f"Warning: Missing or invalid unit for product: {product['name']}")
    product["total_quantity"] = total_quantity if total_quantity else 0
    product["uom"] = uom if uom else "unknown"
    return product



# Merge matched products
def merge_products(products):
    merged = {
        "name": products[0]["name"],
        "brand": products[0]["brand"],
        "unit": products[0]["unit"],
        "platforms": []
    }
    for product in products:
        platform_data = {
            "platform": product["platform"],
            "price": product["price"],
            "mrp": product["mrp"],
            "discount": product["mrp"] - product["price"],
            "product_id": product["product_id"],
            "inventory": product["inventory"],
            "image_url": product.get("image_url", product.get("image_urls", []))
        }
        merged["platforms"].append(platform_data)
    return merged

# Fuzzy match and group products
def match_and_group_products(products, threshold=80):
    normalized = [normalize_product(p) for p in products]
    grouped = []
    visited = set()

    for i, product in enumerate(normalized):
        if i in visited:
            continue
        group = [product]
        visited.add(i)

        for j, other_product in enumerate(normalized[i + 1 :], start=i + 1):
            if j in visited:
                continue

            # Match by name, brand, and unit
            name_match = fuzz.token_set_ratio(product["name"], other_product["name"]) >= threshold
            brand_match = fuzz.ratio(product["brand"], other_product["brand"]) >= threshold
            unit_match = product["total_quantity"] == other_product["total_quantity"] and product["uom"] == other_product["uom"]

            if name_match and brand_match and unit_match:
                group.append(other_product)
                visited.add(j)

        grouped.append(merge_products(group))
    return grouped


app = Flask(__name__)
cors = CORS(app)

@app.route('/search', methods=['GET'])
@cross_origin()
def search():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    query = request.args.get('query')

    if not all([latitude, longitude, query]):
        return jsonify({'error': 'Please provide latitude, longitude, and query parameters.'}), 400

    try:
        swiggy_data = swiggy_search(query, latitude, longitude)
        if not swiggy_data:
            swiggy_data = {'error': 'No data found for Swiggy'}
    except Exception as e:
        swiggy_data = {'error': str(e)}

    try:
        zeptonow_data = zeptonow_search(query, latitude, longitude)
        if not zeptonow_data:
            zeptonow_data = {'error': 'No data found for Zeptonow'}
    except Exception as e:
        zeptonow_data = {'error': str(e)}

    try:
        blinkit_data = blinkit_search(query, latitude, longitude)
        if not blinkit_data:
            blinkit_data = {'error': 'No data found for Blinkit'}
    except Exception as e:
        blinkit_data = {'error': str(e)}

    print(blinkit_data, "blinkit_data")

    data = {
        'swiggy': swiggy_data,
        'zeptonow': zeptonow_data,
        'blinkit': blinkit_data
    }

    blinkit_products = extract_blinkit_products(data)
    swiggy_products = extract_swiggy_products(data)
    zeptonow_products = extract_zeptonow_products(data)

    print(blinkit_products, "blinkit_products")

    # Combine all products
    all_products = blinkit_products + swiggy_products + zeptonow_products
    grouped_products = match_and_group_products(all_products)
    return jsonify(grouped_products)

if __name__ == '__main__':
    app.run(debug=True)