// SPDX-License-Identifier: LGPL-2.1
/*
 * utils.cpp
 *
 * Copyright 2023 Qtechnology A/S
 *
 * Daniel Lundberg Pedersen <dlp@qtec.com>
 */
#include "utils.h"

namespace qamlib
{
/*
 * Utils
 */
std::string name_to_key(const std::string &name)
{
	auto res = std::string();
	bool add_underscore = false;
	res.reserve(name.size());
	for (const auto &c : name) {
		if (isalnum(c)) {
			if (add_underscore) {
				res.push_back('_');
				add_underscore = false;
			}
			res.push_back(tolower(c));
		} else {
			add_underscore = true;
		}
	}
	return res;
}

/**
 *
 * This function is for converting `errno` to different exception types.
 * E.g. EBUSY -> V4L2BusyException. It will always throw an exception derived
 * from V4L2Exception.
 */
void v4l2_exception(const std::string &msg, int err_num)
{
	switch (err_num) {
	case EBUSY:
		throw V4L2BusyException(msg);
	default:
		throw V4L2Exception(msg, err_num);
	};
}
} // namespace qamlib
