from jira import JIRA
import getpass


class JIRATool():
    jira = None

    def auth(self, host, user=None, passwd=None):
        if user is None:
            user = input('username:')
        if passwd is None:
            passwd = getpass.getpass(prompt='password:')
        self.jira = JIRA(server=host, basic_auth=(user, passwd))

    def create_ticket(self, project_key, summary, issuetype, description):
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'issuetype': {'name': issuetype},
            'description': description,
        }
        return self.jira.create_issue(fields=issue_dict)

    def query_issues(self, query_str, max_results=500):
        return self.jira.search_issues(query_str, startAt=0, maxResults=max_results, validate_query=True)

    def get_issue(self, issue_id):
        return self.jira.issue(issue_id)

    def get_issues(self, query_str):
        # default limit for each page is 100
        issues_list = self.query_issues(query_str)
        return [self.get_issue(issue.id) for issue in issues_list]

    def print_issue(self, issue):
        print(issue.key)
        print(issue.__dict__)

    def show_summary(self, issue):
        print(u"key:{0}, summary:{1}".format(issue.key, issue.fields.summary))

    def print_fields(self, issue):
        for field_name in issue.raw.get('fields', []):
            print(u"field:{0}, value:{1}".format(field_name, issue.raw.get('fields').get(field_name, None)))

    def get_field(self, issue, field_name):
        try:
            return issue.raw.get('fields').get(field_name, None)
        except Exception as e:
            print(e)
            return None

    def get_reporter_name(self, issue):
        try:
            return self.get_field(issue, 'reporter').get('name', None)
        except Exception as e:
            return None

    def get_assignee_name(self, issue):
        try:
            return self.get_field(issue, 'assignee').get('name', None)
        except Exception as e:
            return None

    def show_detail1(self, issue):
        detail1 = u"""key:{key}; summary:{summary}; originalEstimate:{originalEstimate}
description:
{description}
"""
        try:
            print(detail1.format(
                key=issue.key,
                summary=self.get_field(issue, 'summary'),
                originalEstimate=self.get_field(issue, 'timetracking').get('originalEstimate', None),
                description=self.get_field(issue, 'description')))
        except Exception as e:
            print(e)

    def assignee_to_reporter(self, issue):
        reporter_name = self.get_reporter_name(issue)
        assignee_name = self.get_assignee_name(issue)
        if not assignee_name and reporter_name:
            try:
                issue.update(assignee={'name': reporter_name})
            except Exception as e:
                print(e)

    def issues_to_csv(self, issues):
        import csv
        with open('issues.csv', 'w', encoding='utf-8') as csvfile:
            issuewrtr = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            issuewrtr.writerow(["key", "summary", "timetracking.originalEstimate", "description"])
            for issue in issues:
                issuewrtr.writerow([
                    issue.key,
                    self.get_field(issue, 'summary'),
                    self.get_field(issue, 'timetracking').get('originalEstimate', None),
                    self.get_field(issue, 'description')
                ])
