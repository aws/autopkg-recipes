#!/usr/local/autopkg/python

import json
import re
from autopkglib import ProcessorError
from autopkglib.URLGetter import URLGetter

__all__ = ["WickrURLProvider"]


class WickrURLProvider(URLGetter):
    """
    Downloads the latest indexmap for all corretto releases, provides url and version of choosen
    major_version + architecture

    Requires version 1.4.
    """

    input_variables = {
        "api_url": {
            "required": False,
            "description": "API URL for getting the download url",
            "default": "http://enterprise-download.wickr.com/api/download",
        },
        "api_type": {
            "required": False,
            "description": "API to hit for getting the download url, either pro or enterprise",
            "default": "Enterprise",
        }
    }
    output_variables = {
        "url": {"description": "Download URL for specified version and architecture"},
        "filename": {"description": "Filename for URLDownload"}
    }
    description = __doc__

    def main(self):
        """
        Provides download url and version
        """
        headers = {
            "Content-Type": "application/json",
        }
        api_type = self.env["api_type"].capitalize()
        self.output(f"Switching Wickr Type to {api_type}")
        data = json.dumps({"name": f"Wickr-{api_type}-Mac-Production"})

        # curl options
        curl_opts = [
            "--url",
            self.env["api_url"],
            "--request",
            "POST",
            "--data",
            data,
        ]
        curl_cmd = self.prepare_curl_cmd()
        self.add_curl_headers(curl_cmd, headers)
        curl_cmd.extend(curl_opts)
        response = self.download_with_curl(curl_cmd)
        result = json.loads(response)
        filename = re.search(r"(Wickr).*(dmg)", result)[0]
        self.env["url"] = result
        self.env["filename"] = filename


if __name__ == "__main__":
    PROCESSOR = WickrURLProvider()
    PROCESSOR.execute_shell()
