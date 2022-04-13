import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import re


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://sochi.hh.ru/vacancies/podrabotka?part_time=employment_project&part_time=employment_part&part_time=temporary_job_true&part_time=from_four_to_six_hours_in_a_day&part_time=only_saturday_and_sunday&part_time=start_after_sixteen&search_field=name&search_field=company_name&search_field=description&clusters=true&enable_snippets=true&ored_clusters=true&hhtmFrom=vacancy_search_list'
                  ,'https://sochi.hh.ru/vacancies/podrabotka?area=53&part_time=employment_project&part_time=employment_part&part_time=temporary_job_true&part_time=from_four_to_six_hours_in_a_day&part_time=only_saturday_and_sunday&part_time=start_after_sixteen&search_field=name&search_field=company_name&search_field=description&clusters=true&enable_snippets=true&ored_clusters=true&hhtmFrom=vacancy_search_list']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name_value = response.css('h1::text').get()
        salary_value = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        url_value = response.url

        if salary_value:
            if salary_value[0] == 'от ':
                salary_min = self.str_to_num(salary_value[1])
                if salary_value[2] == ' до ':
                    salary_max = self.str_to_num(salary_value[3])
                    salary_curr = salary_value[5]
                else:
                    salary_max = None
                    salary_curr = salary_value[3]
            elif salary_value[0] == ' до ':
                salary_min = None
                salary_max = self.str_to_num(salary_value[1])
                salary_curr = salary_value[3]
            else:
                salary_min = self.str_to_num(salary_value[0])
                salary_max = self.str_to_num(salary_value[2])
                salary_curr = salary_value[3]

        yield JobparserItem(name=name_value, salary=salary_value, salary_min=salary_min, salary_max=salary_max, salary_curr=salary_curr, url=url_value)

    def str_to_num(self, str):
        num = re.findall(r'\d+', str)
        return int(''.join(num))
