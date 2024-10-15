# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from check_rekognition_test_tool import CheckRekognitionTestTool


def test_check_content_moderation_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_content_moderation_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_content_moderation',
        'ContentModerationError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_celebrity_recognition_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_celebrity_recognition_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_celebrity_recognition',
        'CelebrityRecognitionError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_face_detection_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_face_detection_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_face_detection',
        'FaceDetectionError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_face_search_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_face_search_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_face_search',
        'FaceSearchError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_label_detection_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_label_detection_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_label_detection',
        'LabelDetectionError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_person_tracking_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_person_tracking_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_person_tracking',
        'PersonTrackingError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_shot_detection_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_shot_detection_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_segment_detection',
        'LabelDetectionError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_technical_cue_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_technical_cue_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_segment_detection',
        'TechnicalCueDetectionError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e


def test_check_text_detection_status():
    import rekognition.check_rekognition_status as lambda_function
    import MediaInsightsEngineLambdaHelper
    import helper

    lambda_handler = lambda_function.check_text_detection_status

    test_tool = CheckRekognitionTestTool(
        lambda_function,
        lambda_handler,
        MediaInsightsEngineLambdaHelper.MasExecutionError,
        helper,
        'get_text_detection',
        'TextDetectionError'
    )
    try:
        test_tool.run_tests()
    except AssertionError as assertion_error:
        raise assertion_error
    except Exception as e:
        raise e
