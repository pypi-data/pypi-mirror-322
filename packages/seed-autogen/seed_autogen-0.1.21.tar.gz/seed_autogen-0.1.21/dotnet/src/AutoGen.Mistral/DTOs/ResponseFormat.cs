﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2ai/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// ResponseFormat.cs

using System.Text.Json.Serialization;

namespace AutoGen.Mistral;

public class ResponseFormat
{
    [JsonPropertyName("type")]
    public string ResponseFormatType { get; set; } = "json_object";
}
