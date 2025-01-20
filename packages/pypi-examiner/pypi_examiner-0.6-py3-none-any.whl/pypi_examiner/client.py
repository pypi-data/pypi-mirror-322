from requests_html import HTMLSession


class examiner(object):
    def __init__(self, timeout=30, retries=3, wait_time=5, sleep_time=5):
        self.session = HTMLSession(mock_browser=True)
        self.timeout = timeout
        self.retries = retries
        self.wait_time = wait_time
        self.sleep_time = sleep_time
        pass

    def _fetch_package_page(self, package_name):
        url = f"https://pypi.org/project/{package_name}/"
        request = self.session.get(url)
        request.html.render(
            timeout=self.timeout,
            retries=self.retries,
            wait=self.wait_time,
            sleep=self.sleep_time,
            reload=True,
        )
        return request

    def _fetch_user_page(self, user_name):
        url = f"https://pypi.org/user/{user_name}/"
        request = self.session.get(url)
        request.html.render(
            timeout=self.timeout,
            retries=self.retries,
            wait=self.wait_time,
            sleep=self.sleep_time,
            reload=True,
        )
        return request

    def _strip_and_validate(self, href, split_len, prefix, select, suffix):
        href_components = href.split("/")

        if not len(href_components) == split_len:
            return False

        if not href.startswith(prefix):
            return False

        if not href.endswith(suffix):
            return False

        return href_components[select]

    def maintained_by(self, user_name):
        result = self._fetch_user_page(user_name)

        # may return 1. nothing 2. an HTML snippet
        packages_section = result.html.find(".package-list", first=True)

        # eliminate 1.
        if not packages_section:
            return []

        packages = set()

        # use 2. to safely extract all packages from the HTML snippet
        for href in packages_section.absolute_links:
            package = self._strip_and_validate(
                href, 6, "https://pypi.org/project/", 4, "/"
            )
            if package:
                packages.add(package)

        return list(packages)

    def who_maintains(self, package_name):
        result = self._fetch_package_page(package_name)

        # may return 1. nothing 2. an HTML snippet or 3. more than one HTML snippets as a list
        maintainer_finder = result.html.find(".sidebar-section__maintainer")

        # eliminate 1.
        if not maintainer_finder:
            return []

        maintainers = set()

        # resolve any 2. to 3.
        if not isinstance(maintainer_finder, list):
            maintainer_sections = [maintainer_finder]
        else:
            maintainer_sections = maintainer_finder

        # use 3. to safely extract data
        for maintainer_section in maintainer_sections:
            for href in maintainer_section.absolute_links:
                user = self._strip_and_validate(
                    href, 6, "https://pypi.org/user/", 4, "/"
                )
                if user:
                    maintainers.add(user)

        return list(maintainers)
