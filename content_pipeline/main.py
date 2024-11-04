from datetime import datetime

from database_operation import ContetIngestionMongoDB
from web_scrapper import web_scrapper
from websearch import brave_search
from chains.web_info_summarization_chain import web_content_summarization_chain
from chains.content_question_pairs_generator_chain import question_from_content

def main():
    db = ContetIngestionMongoDB()

    retrieved_list_of_doc = db.question_retriever()[0:20]
    print("A list of " + str(len(retrieved_list_of_doc)) + ' documents are retrieved from the database')

    current_date = str(datetime.now())[0:10]

    list_of_processed_doc = []

    list_of_new_doc = []
    
    for question_doc in retrieved_list_of_doc:

        question = question_doc["text"]

        list_of_related_websites = brave_search(question, num_results=3, freshness=f"2020-10-09to{current_date}")

        web_content = ""

        list_of_url = []

        for index, web in enumerate(list_of_related_websites):
            web_all_info = web_scrapper(web["URL"])

            doc = {
                "url": web["URL"],
                "title": web['Title'],
                "description": web_all_info
            }
            db.store_web_info(doc)

            list_of_url.append(web["URL"]) 

            web_summary = web_content_summarization_chain().invoke(doc)

            web_content = web_content + f"Source No.{index+1}\n" + web_summary + '\n'
        
        result_of_scope_expansion = question_from_content().invoke({"text":web_content,"question": question})
        
        ans_to_org_question = result_of_scope_expansion.org_question_answer

        new_question_answer_pairs = result_of_scope_expansion.additional_quiestion_answer_pairs

        for question in new_question_answer_pairs.keys():
            new_doc = {
                "question": question,
                "ans": new_question_answer_pairs[question],
                "web": list_of_url
            }
            list_of_new_doc.append(new_doc)
            print(new_doc)
            print("------------new doc-------------")

        org_doc={
            "doc": question_doc,
            "ans": ans_to_org_question,
            "web": list_of_url
        }

        annotation = {
            "question" : question_doc["text"],
            "ans": ans_to_org_question,
            "web": list_of_url
        }
        list_of_processed_doc.append(org_doc)
        print(annotation)
        print("------------old doc-------------")


    db.update_database(list_of_processed_doc,list_of_new_doc)
    print("All documents are successfully updated to database.")
    

if __name__=="__main__":
    main()