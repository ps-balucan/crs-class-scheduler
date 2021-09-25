import json
import genetic_algorithm

def main(event, context):
    try:
        sample_input = event["multiValueQueryStringParameters"]["message[]"]#json.loads(event["queryStringParameters"]["message"])
        length = len(sample_input)
        for i in range(0,length):
            sample_input[i] = sample_input[i].replace("+", " ")
        mycsv = genetic_algorithm.load_csv()
        possible_subjects = []
        subjectList = []
        for input in sample_input:
            newSubject = genetic_algorithm.Subject(input)
            possible_subjects.append(genetic_algorithm.filter_subject(mycsv, input))
            for index, row in genetic_algorithm.filter_subject(mycsv, input).iterrows():
                if (row['professor'] == "TBA" or row['professor'] == "CONCEALED"):
                    row['professor'] = "TBA, TBA2"
                print(row['professor'])
                newCourse = genetic_algorithm.Course(row['course number'], row['name'], row['professor'], row['schedule'].split(' ')[1])
                newCourse._meetingDay = genetic_algorithm.parse_schedule(row['schedule'].split(' ')[0])
                newSubject._courses.append(newCourse)
            subjectList.append(newSubject)

        final_list = genetic_algorithm.genetic_algorithm(subjectList)

        
        # print("testing")
        print(event)
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': str(final_list)
        }
       
        # return dict(statusCode=200,
        # #  body = event)
        # return {
        #     'statusCode': 200,
        #     'headers': {'Content-Type': 'application/json'},
        #     'body': str(test)
        # }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body':"Error detected: " + str(e)
        }