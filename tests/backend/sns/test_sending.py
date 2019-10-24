import pytest

from bluejay.backend import SNSBackend


@pytest.fixture
def expected_json(send_event_command):
    obj = send_event_command.payload

    return SNSBackend.compress(obj)


@pytest.fixture
def expected_subject(send_event_command):
    return send_event_command.event_name


def test_backend_takes_a_SendEvent_command(
    send_event_command,
    backend,
    sns_stub,
    topic_arn,
    faker,
    expected_json,
    expected_subject,
):
    sns_stub.add_response(
        "publish",
        {"MessageId": faker.pystr()},
        {
            "TopicArn": topic_arn,
            "Message": expected_json,
            "Subject": expected_subject,
            "MessageStructure": "json",
        },
    )
    result = backend.send(send_event_command)
    assert result.success is True
