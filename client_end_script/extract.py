import re

data = """
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.663***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.765***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.784***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.754***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.768***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.751***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.915***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.972***
[16/Oct/2023:12:37:33 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.034***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.125***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.141***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.032***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.155***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.092***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.113***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.096***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.155***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.191***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.317***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.308***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.627***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.566***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.538***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.584***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.622***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.551***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.553***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.563***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.579***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.868***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.749***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.781***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.832***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.833***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.891***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.842***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.878***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.844***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.858***
[16/Oct/2023:12:37:34 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.916***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.493***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.541***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.823***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.840***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.647***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.659***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.690***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.640***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.650***
[16/Oct/2023:12:37:35 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.698***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.943***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.949***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.960***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.961***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.962***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.964***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.962***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.987***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.986***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.965***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.754***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.922***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.897***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.939***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.049***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.930***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.932***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.945***
[16/Oct/2023:12:37:36 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***0.961***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.022***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.055***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.051***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.052***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.081***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.221***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.211***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.233***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.242***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.370***
[16/Oct/2023:12:37:37 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.370***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.216***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.313***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.329***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.335***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.371***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.512***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.504***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.417***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.644***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.370***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.486***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.459***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.500***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.510***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.826***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.516***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.585***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.615***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.642***
[16/Oct/2023:12:37:38 +0530] GET /api/quiz/CS007.HG/info/ HTTP/1.0***1.679***
"""

# Define a regular expression pattern to extract values between '***'
pattern = r'\*{3}(.*?)\*{3}'

# Find all matches in the data
matches = re.findall(pattern, data)

# Print the extracted values
for match in matches:
    print(match)
