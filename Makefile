# SPDX-License-Identifier: BSD-2-Clause-Patent
# Copyright 2025 Hewlett Packard Enterprise Development LP

NAME      := E3SM-IO
SRC_EXT   := gz
REPO_NAME := E3SM-IO-pkg
PKG_GIT_COMMIT := 76a1c2fabd042423493a455ef3ce72577a3848a2
GITHUB_PROJECT := Parallel-NetCDF/E3SM-IO

TEST_PACKAGES := $(NAME)-mpich-devel $(NAME)-openmpi3-devel

include packaging/Makefile_packaging.mk
