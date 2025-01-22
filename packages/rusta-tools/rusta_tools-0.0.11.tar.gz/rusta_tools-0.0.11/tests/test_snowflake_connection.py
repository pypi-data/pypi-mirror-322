import unittest
from unittest.mock import patch, MagicMock

import os
import sys

current_dir = os.path.dirname(os.path.abspath("C:/Users/DaM2/development/rusta_tools/snow_flake/src/rusta_tools"))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.rusta_tools.snowflake_connection import Snowflake

class TestSnowflakeConnection(unittest.TestCase):

    scrape_data =  {   
                    "ARTICLE_ID": "AA",
                    "ARTICLE_NAME": "AA",
                    "COMPANY": "AA",
                    "ACTIVE_CTR": False,
                    "ACTIVE_WEB": False,
                    "PRODUCT_COORDINATOR": "AA",
                    "LIFE_CYCLE_STATUS": "AA",
                    "DATE": "9999-11-11",
                    "RETAIL_PRICE": 23,
                    "ACTUAL_PRICE": 23,
                    "ARTICLE_FOUND": False,
                    "SEARCH_URL": "rusta.com",
                    "RELATED": False,    
                    "DISCOUNT_TYPE": "None",
                    "PROMOTION_TYPE_WEB": "None",
                    "PROMOTION_TEXT_WEB": "None",
                    "SAVE_AMOUNT": "None", 
                    "VISIBLE_PRICE": 33.4,
                    "PRICE_INFO": "None",
                    "DEPARTMENT": "None",
                    "SALES_AREA": "None"}

    @patch('src.rusta_tools.snowflake_connection.snowflake.connect')
    def test_connect_to_snowflake_campaign_verification(self, mock_snowflake):
        # Arrange
        mock_snowflake.return_value = MagicMock()
        snowflake_instance =  Snowflake()

        # Act
        snowflake_instance.connect_to_snowflake('CAMPAIGN_VERIFICATION')

        # Assert
        mock_snowflake.assert_called_once_with(
            account=snowflake_instance.db_config['snowflake_rusta_dwh']['account'],
            user=snowflake_instance.db_config['snowflake_rusta_dwh']['user'],
            password=snowflake_instance.get_pwd(),
            warehouse=snowflake_instance.db_config['snowflake_rusta_dwh']['warehouse'],
            database=snowflake_instance.db_config['snowflake_rusta_dwh']['database'],
            schema=snowflake_instance.db_config['snowflake_rusta_dwh']['schema'],
            role=snowflake_instance.db_config['snowflake_rusta_dwh']['role']
        )



if __name__ == '__main__':
    unittest.main()