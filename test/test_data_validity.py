# builtin
import os
import sys
import collections
# external
import bs4
import yaml


############################################################
# utils / setup
############################################################


base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(base_dir)
from lib import utils, view_handlers


############################################################
# tests
############################################################


def test_init():
    assert 1 == 1


def test_load_shoot_roles():
    data = utils.load_shoot_roles()
    assert isinstance(data['Ali3n Club Fuck']['Workers'], dict)


def test_load_role_percents():
    data = utils.load_role_percents()
    assert 0 <= data['Performer'] <= 100
    assert 0 <= data['QAPC'] <= 100


def test_get_table():
    data = utils.get_table()
    assert isinstance(data, collections.OrderedDict)
    assert bool(data)


def test_get_first_video_from_table():
    video = list(utils.get_table().items())[0][1]
    assert isinstance(video, dict)
    assert bool(video)


def test_video_add_worker_and_roles():
    shoot_roles = utils.load_shoot_roles()

    video = list(utils.get_table().items())[0][1]

    assert video.get('Workers') is None
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    assert isinstance(video['Workers'], dict)


def test_video_add_role_unscaled_percents():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)

    assert video.get('role percents unscaled') is None
    video = utils.video_add_role_unscaled_percents(video, role_percents)
    assert 0 <= video['role percents unscaled']['QAPC'] <= 100


def test_video_create_scaling_factor():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    video = utils.video_add_role_unscaled_percents(video, role_percents)

    assert video.get('scaling factor') is None
    video = utils.video_create_scaling_factor(video)
    assert 0 <= video.get('scaling factor') <= 1


def test_video_scale_role_percents():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    video = utils.video_add_role_unscaled_percents(video, role_percents)
    video = utils.video_create_scaling_factor(video)

    assert video.get('role percents') is None
    video = utils.video_scale_role_percents(video)
    assert 0 <= video['role percents']['QAPC'] <= 100


def test_scaling_factor_applies_properly():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    video = utils.video_add_role_unscaled_percents(video, role_percents)
    video = utils.video_create_scaling_factor(video)
    video = utils.video_scale_role_percents(video)

    expected_scaled_percent = video['role percents unscaled']['QAPC'] * video['scaling factor']
    scaled_percent = video['role percents']['QAPC']

    assert expected_scaled_percent == scaled_percent


def test_video_get_total_earnings():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    video = utils.video_add_role_unscaled_percents(video, role_percents)
    video = utils.video_create_scaling_factor(video)
    video = utils.video_scale_role_percents(video)

    assert video.get('total earnings') is None
    video = utils.video_get_total_earnings(video)
    assert video.get('total earnings') is not None


def test_video_get_worker_earnings():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    video = utils.video_add_role_unscaled_percents(video, role_percents)
    video = utils.video_create_scaling_factor(video)
    video = utils.video_scale_role_percents(video)
    video = utils.video_get_total_earnings(video)

    assert video.get('earnings') is None
    video = utils.video_get_worker_earnings(video)
    assert isinstance(video.get('earnings'), dict)


def test_validate_earnings():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    video = list(utils.get_table().items())[0][1]
    video = utils.video_add_worker_and_roles(video, shoot_roles)
    video = utils.video_add_role_unscaled_percents(video, role_percents)
    video = utils.video_create_scaling_factor(video)
    video = utils.video_scale_role_percents(video)
    video = utils.video_get_total_earnings(video)
    video = utils.video_get_worker_earnings(video)

    total_earnings = video['total earnings']
    sum_all_earnings = 0
    for earning in video['earnings'].values():
        sum_all_earnings += earning

    assert round(total_earnings, 2) == round(sum_all_earnings, 2)


def test_all_videos():
    shoot_roles = utils.load_shoot_roles()
    role_percents = utils.load_role_percents()

    for video in utils.get_table().values():
        video = utils.video_add_worker_and_roles(video, shoot_roles)
        video = utils.video_add_role_unscaled_percents(video, role_percents)
        video = utils.video_create_scaling_factor(video)
        video = utils.video_scale_role_percents(video)
        video = utils.video_get_total_earnings(video)
        video = utils.video_get_worker_earnings(video)

        total_earnings = video['total earnings']
        sum_all_earnings = 0
        for earning in video['earnings'].values():
            sum_all_earnings += earning

        assert round(total_earnings, 2) == round(sum_all_earnings, 2)


def test_view_handler():
    table = view_handlers.get_and_populate_shoot_table()
    for video in table.values():
        total_earnings = video['total earnings']
        sum_all_earnings = 0
        for earning in video['earnings'].values():
            sum_all_earnings += earning

        assert round(total_earnings, 2) == round(sum_all_earnings, 2)