def get_questions():    
    import requests

    url = "https://leetcode.com/graphql/"
    headers = {
        "Content-Type": "application/json",
        "cookie":'YOUR_COOKIE_VALUE',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    payload = {
        "query": """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                ) {
                    total: totalNum
                    questions: data {
                        acRate
                        difficulty
                        freqBar
                        frontendQuestionId: questionFrontendId
                        isFavor
                        paidOnly: isPaidOnly
                        status
                        title
                        titleSlug
                        topicTags {
                            name
                            id
                            slug
                        }
                        hasSolution
                        hasVideoSolution
                    }
                }
            }
        """,
        "variables": {
            "categorySlug": "all-code-essentials",
            "skip": 0,
            "limit": 50,
            "filters": {}
        },
        "operationName": "problemsetQuestionList"
    }
    response = requests.post(url, json=payload, headers=headers)

    response_json=response.json()
    questions = response_json["data"]["problemsetQuestionList"]["questions"]

    count = 0
    for question in questions:
        if question["status"] is None:
            # question = f"https://leetcode.com/problems/{question['titleSlug']}"
            print(f"https://leetcode.com/problems/{question['titleSlug']}")
            # solve(question)

            count += 1
            if count == 3:
                break
get_questions()