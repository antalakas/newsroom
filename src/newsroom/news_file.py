# src/newsroom/news_file.py
import json


def read_file(fileName, min, max, dict):
    with open(fileName) as json_file:
        data = json.load(json_file)["items"]["item"]
        is_list = isinstance(data, list)

        if not is_list:
            # print(data['items']['item'])
            min, max, dict = analyze_item(data, min, max, dict)
        else:
            for item in data:
                # print(data['items']['item'])
                min, max, dict = analyze_item(item, min, max, dict)

        return min, max, dict


def analyze_item(item, min, max, dict):
    # print('Id: ' + str(item['id']))
    # print('Timestamp: ' + item['modyfication_date'])
    # date_time_obj = datetime.datetime.strptime(item['modyfication_date'], '%Y-%m-%d %H:%M:%S')
    # timestamp = int(datetime.datetime.timestamp(date_time_obj))
    # print('Timestamp: ' + str(timestamp))
    # print('Title: ' + item['title'])
    # print('Medium: ' + item['medium'])

    mediumId = item["medium_id"]
    if mediumId < min:
        min = mediumId

    if mediumId > max:
        max = mediumId

    if mediumId in dict.keys():
        dict[mediumId] = 1 + dict[mediumId]
    else:
        dict[mediumId] = 1

    # print('Medium Id: ' + str(mediumId))
    # print('Medium Group: ' + item['medium_group'])
    # print('Medium Pageviews: ' + str(item['medium_pageviews']))
    # print('Is Blog: ' + str(item['is_blog']))
    # print('Date: ' + item['date'])
    # print('URL: ' + item['url'])
    # print('Advertising ValueE quivalency: ' + str(item['advertising_value_equivalency']))
    # # print('Translations: ' + item['translations'])
    # print('Keyword: ' + item['keyword'])
    # if not isinstance(item['snippet'], dict):
    #     print('Snippet: ' + item['snippet'])
    # if not isinstance(item['text'], dict):
    #     print('Text: ' + item['text'])
    # print('Importance: ' + str(item['importance']))
    # sentiment = str(item['sentiment'])
    # print('Sentiment: ' + int(sentiment))

    # key = str(mediumId) + "_" + str(timestamp)
    # if key in avoid_duplicate_coords:
    #     avoid_duplicate_coords[key] += 1
    # else:
    #     avoid_duplicate_coords[key] = 0
    #     rows.append(mediumId)
    #     columns.append(timestamp)
    #     if not isinstance(item['importance'], dict):
    #         array_data.append(int(item['importance']))
    #     else:
    #         array_data.append(0)
    # print('')
    return min, max, dict


def get_file_stats(fileName, dim_id, num_of_items, medium_dict, stats_dict):
    with open(fileName) as json_file:
        data = json.load(json_file)["items"]["item"]
        is_list = isinstance(data, list)

        if not is_list:
            dim_id, num_of_items, medium_dict, stats_dict = calc_file_stats(
                data, dim_id, num_of_items, medium_dict, stats_dict
            )
        else:
            for item in data:
                dim_id, num_of_items, medium_dict, stats_dict = calc_file_stats(
                    item, dim_id, num_of_items, medium_dict, stats_dict
                )

        return dim_id, num_of_items, medium_dict, stats_dict


def calc_file_stats(item, dim_id, num_of_items, medium_dict, stats_dict):
    mediumId = item["medium_id"]

    if mediumId in stats_dict.keys():
        stats_dict[mediumId] = 1 + stats_dict[mediumId]
    else:
        stats_dict[mediumId] = 1
        dim_id = dim_id + 1
        medium_dict[mediumId] = dim_id

    num_of_items = num_of_items + 1

    return dim_id, num_of_items, medium_dict, stats_dict
