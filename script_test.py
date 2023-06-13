import asyncio

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import Applicant, ApplicantOffer

# from huntflow_api_client.entities import ApplicantsQuestionary
from huntflow_api_client.tokens import ApiToken

# from huntflow_api_client.entities.account_offers import AccountOffer
# from huntflow_api_client.models.request.applicant_offers import ApplicantOfferUpdate
# from huntflow_api_client.models.request.applicants import CreateApplicantLogRequest
# from huntflow_api_client.models.response.account_offers import AccountOfferResponse


# from huntflow_api_client.entities import MailTemplate


# from huntflow_api_client.entities.users import User


# from huntflow_api_client.entities import Resume


class Applicants:
    pass


async def main():
    account_id = 19
    applicant_id = 256
    token = ApiToken(
        access_token="442b3cbc7217a68e0c29eb476c6d4269c57477ee2544334e6ef8da69a63ee22f"
    )
    api = "https://int-131-api.huntflow.dev/v2"
    api_client = HuntflowAPI(api, token=token)
    # resumes = Resume(api_client)

    # response = await resumes.get(account_id, applicant_id, applicant_id)
    # response = await resumes.delete(account_id, applicant_id, applicant_id)
    # response = await resumes.get_resume_sources(account_id)
    # body = ApplicantResumeUpdateData(body="test")
    # data = ApplicantResumeUpdateRequest(account_source=491, data=body)
    # response = await resumes.update(account_id, applicant_id, applicant_id, data)

    # quest = ApplicantsQuestionary(api_client)
    # response = await quest.get(account_id, applicant_id)
    # data = {"english": None}
    # response = await quest.create(account_id, applicant_id, data)
    # response = await quest.update(account_id, applicant_id, data)

    # users = User(api_client)
    # response = await users.get(account_id, 36)
    # temps = MailTemplate(api_client)
    # response = await temps.list(account_id)

    # offers = AccountOffer(api_client)
    # response = await offers.get_account_offers(account_id)
    # response = await offers.get_account_offers_with_schema(account_id, 21)
    # response = await offers.get_pdf(account_id, 413, 14)
    # with open("dsfds.pdf", "wb") as f:
    #     f.write(response)
    #   data = ApplicantOfferUpdate(account_applicant_offer=21, values={
    #   "position_name": "IOS developer",
    #   "offer_text": "Offer text2",
    #   "whom_date": "2023-06-27",
    #   "whom_name": "Test"
    # })
    #   response = await offers.update(account_id, 414, 14, data)
    # response = await offers.get(account_id, 414, 214)
    # print(response)
    # app = Applicant(api_client)
    # data = CreateApplicantLogRequest(comment="Test comment")
    # response = await app.create_log(account_id=account_id, applicant_id=413, data=data)
    offers = ApplicantOffer(api_client)
    response = await offers.get(19, 414, 214, True)
    print(response)

    # a = []
    # print(sorted(a))


if __name__ == "__main__":
    asyncio.run(main())
