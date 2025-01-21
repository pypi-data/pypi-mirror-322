import numpy as np
import cv2
import mediapipe as mp


def get_image_warped(image_original: bytes) -> cv2.typing.MatLike:
    pts_index = list(range(21))
    pts_target_normalized = np.float32(
        [
            [1 - 0.48203104734420776, 0.9063420295715332],
            [1 - 0.6043621301651001, 0.8119394183158875],
            [1 - 0.6763232946395874, 0.6790258884429932],
            [1 - 0.7340714335441589, 0.5716733932495117],
            [1 - 0.7896472215652466, 0.5098430514335632],
            [1 - 0.5655680298805237, 0.5117031931877136],
            [1 - 0.5979393720626831, 0.36575648188591003],
            [1 - 0.6135331392288208, 0.2713503837585449],
            [1 - 0.6196483373641968, 0.19251111149787903],
            [1 - 0.4928809702396393, 0.4982593059539795],
            [1 - 0.4899863600730896, 0.3213786780834198],
            [1 - 0.4894656836986542, 0.21283167600631714],
            [1 - 0.48334982991218567, 0.12900274991989136],
            [1 - 0.4258815348148346, 0.5180916786193848],
            [1 - 0.4033462107181549, 0.3581996262073517],
            [1 - 0.3938145041465759, 0.2616880536079407],
            [1 - 0.38608720898628235, 0.1775170862674713],
            [1 - 0.36368662118911743, 0.5642163157463074],
            [1 - 0.33553171157836914, 0.44737303256988525],
            [1 - 0.3209102153778076, 0.3749568462371826],
            [1 - 0.31213682889938354, 0.3026996850967407],
        ]
    )

    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5
    ) as hands:
        # 1. Extract 21 landmark points
        image_array = np.frombuffer(image_original, dtype=np.uint8)
        image = cv2.flip(cv2.imdecode(image_array, cv2.IMREAD_COLOR), 1)

        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image_height, image_width, _ = image.shape

        if results.multi_hand_landmarks is None:
            raise RuntimeError(
                "Palm lines not properly detected! Please use another palm image."
            )

        else:
            hand_landmarks = results.multi_hand_landmarks[0]

            # 2. Align images
            pts = np.float32(
                [
                    [
                        hand_landmarks.landmark[i].x * image_width,
                        hand_landmarks.landmark[i].y * image_height,
                    ]
                    for i in pts_index
                ]
            )
            pts_target = np.float32(
                [[x * image_width, y * image_height] for x, y in pts_target_normalized]
            )
            M, mask = cv2.findHomography(pts, pts_target, cv2.RANSAC, 5.0)
            warped_image = cv2.warpPerspective(
                image, M, (image_width, image_height), borderMode=cv2.BORDER_REPLICATE
            )

            return warped_image
