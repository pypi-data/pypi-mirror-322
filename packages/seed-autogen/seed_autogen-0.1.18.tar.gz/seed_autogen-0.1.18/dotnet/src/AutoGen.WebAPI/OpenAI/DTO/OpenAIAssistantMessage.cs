﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2ai/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// OpenAIAssistantMessage.cs

using System.Text.Json.Serialization;

namespace AutoGen.WebAPI.OpenAI.DTO;

internal class OpenAIAssistantMessage : OpenAIMessage
{
    [JsonPropertyName("role")]
    public override string? Role { get; } = "assistant";

    [JsonPropertyName("content")]
    public string? Content { get; set; }

    [JsonPropertyName("name")]
    public string? Name { get; set; }

    [JsonPropertyName("tool_calls")]
    public OpenAIToolCallObject[]? ToolCalls { get; set; }
}
