# Make.com Integration Guide

## Setting Up the Scenario

1. Create New Scenario
   - Click "Create a new scenario"
   - Select "HTTP" as your trigger

2. Configure HTTP Request
   - Method: POST
   - URL: Your deployed API endpoint
   - Headers:
     ```
     Content-Type: application/json
     X-API-Key: your_api_key
     ```

3. Request Body Structure
   ```json
   {
     "city": "holland",
     "state": "mi",
     "preferred_language": "English",
     "specialization": "Residential",
     "budget": {
       "min": 140000,
       "max": 550000
     },
     "area_specifics": {
       "include_areas": ["Holland", "Zeeland"],
       "exclude_areas": []
     }
   }
   ```

4. Response Handling
   - Add a JSON parser module
   - Use `$.results[*]` to iterate through results
   - Available fields:
     - name
     - brokerage
     - experience
     - reviews
     - contact
     - office_address

5. Error Handling
   - Check `$.status` for "success" or "error"
   - Error details in `$.error` if status is "error"

## Testing
1. Use the "Test" button in Make.com
2. Verify response format matches expected structure
3. Check logs for any issues

## Common Issues
- Timeout: Increase scenario timeout in Make.com settings
- Rate Limiting: Add delay between requests
- Data Format: Ensure JSON structure matches example 