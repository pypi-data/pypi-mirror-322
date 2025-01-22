﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2ai/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// LLMConfiguration.cs

using AutoGen.OpenAI.V1;

namespace AutoGen.BasicSample;

internal static class LLMConfiguration
{
    public static OpenAIConfig GetOpenAIGPT3_5_Turbo()
    {
        var openAIKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("Please set OPENAI_API_KEY environment variable.");
        var modelId = "gpt-3.5-turbo";
        return new OpenAIConfig(openAIKey, modelId);
    }

    public static OpenAIConfig GetOpenAIGPT4()
    {
        var openAIKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("Please set OPENAI_API_KEY environment variable.");
        var modelId = "gpt-4";

        return new OpenAIConfig(openAIKey, modelId);
    }

    public static AzureOpenAIConfig GetAzureOpenAIGPT3_5_Turbo(string? deployName = null)
    {
        var azureOpenAIKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? throw new Exception("Please set AZURE_OPENAI_API_KEY environment variable.");
        var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? throw new Exception("Please set AZURE_OPENAI_ENDPOINT environment variable.");
        deployName = deployName ?? Environment.GetEnvironmentVariable("AZURE_OPENAI_DEPLOY_NAME") ?? throw new Exception("Please set AZURE_OPENAI_DEPLOY_NAME environment variable.");
        return new AzureOpenAIConfig(endpoint, deployName, azureOpenAIKey);
    }

    public static AzureOpenAIConfig GetAzureOpenAIGPT4(string deployName = "gpt-4")
    {
        var azureOpenAIKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY") ?? throw new Exception("Please set AZURE_OPENAI_API_KEY environment variable.");
        var endpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT") ?? throw new Exception("Please set AZURE_OPENAI_ENDPOINT environment variable.");

        return new AzureOpenAIConfig(endpoint, deployName, azureOpenAIKey);
    }
}
