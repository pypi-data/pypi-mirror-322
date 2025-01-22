""" unit tests for ae.updater portion. """
import os
import shutil
import tempfile

import pytest

from ae.base import INI_EXT, in_wd, norm_path, write_file
from ae.files import read_file_text
from ae.paths import user_data_path
from ae.updater import (
    COPIES_SRC_FOLDER_NAME, MOVES_SRC_FOLDER_NAME, OVERWRITES_SRC_FOLDER_NAME,
    UPDATER_MODULE_NAME, PRE_APP_MODULE_NAME,
    check_copies, check_moves, check_overwrites, check_local_updates, check_local_pre_app_runs, check_all)

FILE0 = "app" + INI_EXT
CONTENT0 = "TEST FILE0 CONTENT"
OLD_CONTENT0 = "OLD/LOCKED FILE0 CONTENT"

DIR1 = 'app_dir'
FILE1 = 'app.png'
CONTENT1 = "TEST FILE1 CONTENT"


@pytest.fixture(params=[COPIES_SRC_FOLDER_NAME, MOVES_SRC_FOLDER_NAME, OVERWRITES_SRC_FOLDER_NAME])
def files_to_move(request, tmpdir):
    """ create test files in source directory to be moved and/or overwritten. """
    src_dir = tmpdir.mkdir(request.param)

    src_file1 = src_dir.join(FILE0)
    src_file1.write(CONTENT0)
    src_sub_dir = src_dir.mkdir(DIR1)
    src_file2 = src_sub_dir.join(FILE1)
    src_file2.write(CONTENT1)

    yield str(src_file1), str(src_file2)

    # tmpdir/dst_dir1 will be removed automatically by pytest - leaving the last three temporary directories
    # .. see https://docs.pytest.org/en/latest/tmpdir.html#the-default-base-temporary-directory
    # shutil.rmtree(tmpdir)


def _create_file_at_destination(dst_folder):
    """ create file0 at destination folder to block move. """
    dst_file = os.path.join(dst_folder, FILE0)
    write_file(dst_file, OLD_CONTENT0)
    return dst_file


class TestFileUpdates:
    def test_copies_to_parent_dir(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_move:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        copied_files = check_copies(src_folder=src_dir, dst_folder=dst_dir)
        for src_file_path in files_to_move:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in copied_files

        if COPIES_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_move:
                assert os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_blocked_copies_to_parent_dir(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_move:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        assert len(check_moves(src_folder=src_dir, dst_folder=dst_dir)) == 1

        if COPIES_SRC_FOLDER_NAME in src_dir:
            assert os.path.exists(files_to_move[0])
            assert read_file_text(files_to_move[0]) == CONTENT0
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_move[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == OLD_CONTENT0

            assert not os.path.exists(files_to_move[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_move[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1

    def test_moves_to_parent_dir(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_move:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        moved_to_files = check_moves(src_folder=src_dir, dst_folder=dst_dir)
        for src_file_path in files_to_move:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in moved_to_files

        if MOVES_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_move:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_blocked_moves_to_parent_dir(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_move:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        assert len(check_moves(src_folder=src_dir, dst_folder=dst_dir)) == 1

        if MOVES_SRC_FOLDER_NAME in src_dir:
            assert os.path.exists(files_to_move[0])
            assert read_file_text(files_to_move[0]) == CONTENT0
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_move[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == OLD_CONTENT0

            assert not os.path.exists(files_to_move[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_move[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1

    def test_overwrites_to_parent_dir(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = os.path.join(src_dir, '..')
        for src_file_path in files_to_move:
            assert os.path.exists(src_file_path)
            assert not os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

        moved_to_files = check_overwrites(src_folder=src_dir, dst_folder=dst_dir)
        for src_file_path in files_to_move:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in moved_to_files

        if OVERWRITES_SRC_FOLDER_NAME in src_dir:
            for src_file_path in files_to_move:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))

    def test_unblocked_overwrites_to_parent_dir(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = os.path.join(src_dir, '..')
        dst_block_file = _create_file_at_destination(dst_dir)
        assert os.path.exists(dst_block_file)
        for src_file_path in files_to_move:
            assert os.path.exists(src_file_path)
            dst_file = os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))
            assert dst_file == dst_block_file or not os.path.exists(dst_file)

        moved_to_files = check_overwrites(src_folder=src_dir, dst_folder=dst_dir)
        for src_file_path in files_to_move:
            assert norm_path(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir))) in moved_to_files

        if OVERWRITES_SRC_FOLDER_NAME in src_dir:
            assert not os.path.exists(files_to_move[0])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_move[0], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT0

            assert not os.path.exists(files_to_move[1])
            dst_file = os.path.join(dst_dir, os.path.relpath(files_to_move[1], src_dir))
            assert os.path.exists(dst_file)
            assert read_file_text(dst_file) == CONTENT1


def _create_module(tmp_dir, module_name):
    fn = os.path.join(tmp_dir, module_name + '.py')
    write_file(fn, """def run_updater():\n    return True""")

    return fn


@pytest.fixture
def created_run_updater():
    """ create test module to be executed. """
    with tempfile.TemporaryDirectory() as tmp_dir, in_wd(tmp_dir):
        yield _create_module(tmp_dir, UPDATER_MODULE_NAME)


@pytest.fixture
def created_pre_app_run():
    """ create test module to be executed. """
    with tempfile.TemporaryDirectory() as tmp_dir, in_wd(tmp_dir):
        yield _create_module(tmp_dir, PRE_APP_MODULE_NAME)


class TestRunUpdater:
    def test_updater(self, created_run_updater):
        assert os.path.exists(created_run_updater)
        check_local_updates()
        assert not os.path.exists(created_run_updater)

    def test_pre_app_runs(self, created_pre_app_run):
        assert os.path.exists(created_pre_app_run)
        check_local_pre_app_runs()
        assert os.path.exists(created_pre_app_run)


class TestCheckAll:
    def test_nothing_to_do(self):
        with tempfile.TemporaryDirectory() as tmp_dir, in_wd(tmp_dir):
            check_all()

    def test_file_copies_to_user_dir_via_check_all(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = user_data_path()

        copied = []
        try:
            copied += check_all(copy_src_folder=src_dir)

            for src_file_path in files_to_move:
                assert os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in copied:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_file_moves_to_user_dir_via_check_all(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = user_data_path()

        moved = []
        try:
            moved += check_all(move_src_folder=src_dir)

            for src_file_path in files_to_move:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in moved:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_file_overwrites_to_user_dir_via_check_all(self, files_to_move):
        src_dir = os.path.dirname(files_to_move[0])
        dst_dir = user_data_path()

        moved = []
        try:
            moved += check_all(over_src_folder=src_dir)

            for src_file_path in files_to_move:
                assert not os.path.exists(src_file_path)
                assert os.path.exists(os.path.join(dst_dir, os.path.relpath(src_file_path, src_dir)))
        finally:
            for dst_file_path in moved:
                dst_path = os.path.relpath(dst_file_path, dst_dir)
                if os.path.exists(dst_file_path):
                    os.remove(dst_file_path)
                    if dst_path != os.path.basename(dst_file_path):
                        shutil.rmtree(os.path.dirname(dst_file_path))

    def test_updater_via_check_all(self, created_run_updater):
        assert os.path.exists(created_run_updater)
        check_all()
        assert not os.path.exists(created_run_updater)

    def test_pre_app_runs_via_check_all(self, created_pre_app_run):
        assert os.path.exists(created_pre_app_run)
        check_all()
        assert os.path.exists(created_pre_app_run)
