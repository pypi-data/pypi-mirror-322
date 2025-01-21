from fixa import Test, Agent, Scenario, Evaluation, TestRunner
from fixa.evaluators import LocalEvaluator
from dotenv import load_dotenv
import ngrok, os, asyncio

load_dotenv(override=True)

async def main():
    agent = Agent(
        name="jessica",
        prompt="you are a young woman named lily who says 'like' a lot",
        voice_id="b7d50908-b17c-442d-ad8d-810c63997ed9"
    )

    scenario = Scenario(
        name="order_donut",
        prompt="order a dozen donuts with sprinkles and a coffee",
        evaluations=[
            Evaluation(name="order_success", prompt="the order was successful"),
            Evaluation(name="price_confirmed", prompt="the agent confirmed the price of the order"),
        ],
    )

    port = 8765
    listener = await ngrok.forward(port, authtoken=os.getenv("NGROK_AUTH_TOKEN"), domain="api.jpixa.ngrok.dev") # type: ignore (needed or else python will complain)

    test_runner = TestRunner(
        port=port,
        ngrok_url=listener.url(),
        twilio_phone_number=os.getenv("TWILIO_PHONE_NUMBER") or "", # the twilio phone number to initiate calls from
        evaluator=LocalEvaluator(),
    )

    test = Test(scenario=scenario, agent=agent)
    test_runner.add_test(test)

    result = await test_runner.run_tests(
        type=TestRunner.OUTBOUND,
        phone_number=os.getenv("TEST_PHONE_NUMBER") or "", # the phone number to call
    )

if __name__ == "__main__":
    asyncio.run(main())
