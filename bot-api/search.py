import requests
from lxml import html


def search_answers(to_search, answer_limit):
    print('Debug Assistant> Looking for answers right now...')

    # Get a list of 'answer_limit' StackOverflow questions related to the user's input
    query = {
        'page': 1,
        'pagesize': answer_limit,
        'order': 'desc',
        'sort': 'votes',
        'title': to_search,
        'site': 'stackoverflow'
    }
    response = requests.get(
        'https://api.stackexchange.com/2.3/search/advanced', params=query)

    # Iterate through the list of questions
    answer_list = list()
    content = response.json()
    for item in content['items']:
        # Filter the ones which have answers
        if item['is_answered'] is True:
            question = item['title']
            question_id = item['question_id']
            print(question)

            # Find the id of the most upvoted answer for this question
            query = {
                'pagesize': 1,
                'order': 'desc',
                'sort': 'votes',
                'site': 'stackoverflow'
            }
            res1 = requests.get(
                f'https://api.stackexchange.com/2.3/questions/{question_id}/answers', params=query)

            answer_id = res1.json()['items'][0]['answer_id']

            # Access the page of this question&answer and extract the HTML for parsing
            res2 = requests.get(f'https://stackoverflow.com/a/{answer_id}')
            tree = html.fromstring(res2.content)

            # Filter to find only the div containing the best/most upvoted answer
            best_answer_element = tree.xpath(
                '//div[@class="answer js-answer accepted-answer"]')[0]

            # Further filter to find the div containing the answer text
            best_answer_raw_text_element = best_answer_element.xpath(
                './/div[@class="s-prose js-post-body"]')[0].text_content()

            # Append question, answer text and link to answer list
            answer_list.append(
                (question, best_answer_raw_text_element.strip(), f'https://stackoverflow.com/a/{answer_id}'))

    print('Debug Assistant> Got it! Here...')
    return answer_list


if __name__ == '__main__':
    ex = search_answers('segmentation fault', 5)
    for ans in ex:
        print(ans)
