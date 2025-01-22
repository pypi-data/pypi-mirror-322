# SPDX-FileCopyrightText: Copyright (c) 2025 Xronos Inc.
# SPDX-License-Identifier: LicenseRef-Xronos-Commercial-License-v1

import xronos._runtime as runtime

class OtelTelemetryBackend(runtime.TelemetryBackend):
    def __init__(
        self,
        attribute_manager: runtime.AttributeManager,
        application_name: str,
        endpoint: str,
        hostname: str,
        pid: int,
    ) -> None: ...
