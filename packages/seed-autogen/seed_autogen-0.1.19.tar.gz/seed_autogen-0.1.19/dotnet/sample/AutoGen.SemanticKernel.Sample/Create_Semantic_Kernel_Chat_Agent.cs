﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2ai/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// Create_Semantic_Kernel_Chat_Agent.cs

#region Using
using AutoGen.Core;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
#endregion Using
namespace AutoGen.SemanticKernel.Sample;

public class Create_Semantic_Kernel_Chat_Agent
{
    public static async Task RunAsync()
    {
        #region Create_Kernel
        var openAIKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new Exception("Please set OPENAI_API_KEY environment variable.");
        var modelId = "gpt-3.5-turbo";
        var kernel = Kernel.CreateBuilder()
            .AddOpenAIChatCompletion(modelId: modelId, apiKey: openAIKey)
            .Build();
        #endregion Create_Kernel

        #region Create_ChatCompletionAgent
        // The built-in ChatCompletionAgent from semantic kernel.
        var chatAgent = new ChatCompletionAgent()
        {
            Kernel = kernel,
            Name = "assistant",
            Description = "You are a helpful AI assistant",
        };
        #endregion Create_ChatCompletionAgent

        #region Create_SemanticKernelChatCompletionAgent
        var messageConnector = new SemanticKernelChatMessageContentConnector();
        var skAgent = new SemanticKernelChatCompletionAgent(chatAgent)
            .RegisterMiddleware(messageConnector) // register message connector so it support AutoGen built-in message types like TextMessage.
            .RegisterPrintMessage(); // pretty print the message to the console
        #endregion Create_SemanticKernelChatCompletionAgent

        #region Send_Message
        await skAgent.SendAsync("Hey tell me a long tedious joke");
        #endregion Send_Message
    }
}
