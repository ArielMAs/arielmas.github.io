# Source the .env file
source secrets.env

EMAIL=$SCRAPER_EMAIL
AUTH_KEY=$SCRAPER_AUTH
BASE_URL="https://data.usajobs.gov/api/search"
ROWS_PER_PAGE=500
MAX_ROWS=10000
PAGE=1
echo running
echo '[]' > main.json

# Loop through pages until we reach the max rows or no more results
echo "Connection to API started"
while true; do
    # Make the request for the current page
    curl -H "Host: data.usajobs.gov" \
         -H "User-Agent: $EMAIL" \
         -H "Authorization-Key: $AUTH_KEY" \
         "$BASE_URL?page=$PAGE&ResultsPerPage=$ROWS_PER_PAGE&DatePosted=60" \
         -o "page_$PAGE.json"
    
    RESULT_COUNT=$(jq '.SearchResult.SearchResultCount' "page_$PAGE.json")

    jq '[.SearchResult.SearchResultItems[].MatchedObjectDescriptor 
        | {PositionID, PositionTitle, PositionLocationDisplay, PositionLocation, OrganizationName, DepartmentName, JobCategory, QualificationSummary, PositionRemuneration, PublicationStartDate, UserArea: {Details: {JobSummary: .UserArea.Details.JobSummary, MajorDuties: .UserArea.Details.MajorDuties}}}]' \
        "page_$PAGE.json" > "tmp.json" && mv tmp.json "page_$PAGE.json"

    # Merge the current page data into main.json
    jq -s 'add' main.json "page_$PAGE.json" > "tmp.json" && mv tmp.json main.json
    
    #Clean
    rm page_$PAGE.json
    # Break if no more results or max rows reached
    if [ "$RESULT_COUNT" -lt $ROWS_PER_PAGE ]; then
        break
    fi
    echo "Page: "$PAGE
    echo "Result Count: "$RESULT_COUNT
    # Increment page number
    PAGE=$((PAGE + 1))
done
echo "Connection to API ended. Long JSON is ready."
