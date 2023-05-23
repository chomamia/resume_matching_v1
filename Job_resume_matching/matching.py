import pandas as pd
import json
# from Rules import Rules
from Job_resume_matching.Rules import Rules
import ast


def modifying_type_resume(resumes):
    for i in range(len(resumes["degrees"])):
        resumes["degrees"][i] = ast.literal_eval(resumes["degrees"][i])
    for i in range(len(resumes["skills"])):
        resumes["skills"][i] = ast.literal_eval(resumes["skills"][i])
    return resumes


def modifying_type_job(jobs):
    for i in range(len(jobs["Skills"])):
        jobs["Skills"][i] = ast.literal_eval(jobs["Skills"][i])
    return jobs

def transform_dataframe_to_json(dataframe):
    # transforms the dataframe into json
    result = dataframe.to_json(orient="records")
    parsed = json.loads(result)
    json_data = json.dumps(parsed, indent=4)

    return json_data

def matching(jobs, resumes):
    with open('Resources/data/labels.json') as fp:
            labels = json.load(fp)
    # jobs = pd.read_csv('Resources/data/job_description_by_spacy.csv', index_col=0)
    # resumes = pd.read_csv('Resources/data/resumes_by_spacy.csv', index_col=0)
    resumes = modifying_type_resume(resumes)
    # jobs = modifying_type_job(jobs)
    rules = Rules(labels, resumes, jobs)
    resumes_matched_jobs = pd.DataFrame()
    for job_index in range(len(jobs)):
        resumes_matched = rules.matching_score(resumes, jobs, job_index)
        # resumes_matched_jobs = resumes_matched_jobs.append(resumes_matched)
        resumes_matched_jobs = pd.concat([resumes_matched_jobs, resumes_matched])
    # resumes_matched_json = transform_dataframe_to_json(resumes_matched_jobs)
    resumes_matched_jobs = resumes_matched_jobs.sort_values(by=["matching score job 0"], ascending=False)
    return resumes_matched_jobs

def main():
    results = matching()
    print(results)

if __name__ == '__main__':
    main()