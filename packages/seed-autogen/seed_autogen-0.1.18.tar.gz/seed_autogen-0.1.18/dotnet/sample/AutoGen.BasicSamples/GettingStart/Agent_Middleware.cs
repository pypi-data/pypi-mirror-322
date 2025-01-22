﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2ai/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// Agent_Middleware.cs

#region Using
using AutoGen.Core;
using AutoGen.OpenAI.V1;
using AutoGen.OpenAI.V1.Extension;
using Azure.AI.OpenAI;
#endregion Using
using FluentAssertions;

namespace AutoGen.BasicSample;

public class Agent_Middleware
{
    public static async Task RunTokenCountAsync()
    {
        #region Create_Agent
        var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new InvalidOperationException("Please set the environment variable OPENAI_API_KEY");
        var model = "gpt-3.5-turbo";
        var openaiClient = new OpenAIClient(apiKey);
        var openaiMessageConnector = new OpenAIChatRequestMessageConnector();
        var totalTokenCount = 0;
        var agent = new OpenAIChatAgent(
            openAIClient: openaiClient,
            name: "agent",
            modelName: model,
            systemMessage: "You are a helpful AI assistant")
            .RegisterMiddleware(async (messages, option, innerAgent, ct) =>
            {
                var reply = await innerAgent.GenerateReplyAsync(messages, option, ct);
                if (reply is MessageEnvelope<ChatCompletions> chatCompletions)
                {
                    var tokenCount = chatCompletions.Content.Usage.TotalTokens;
                    totalTokenCount += tokenCount;
                }
                return reply;
            })
            .RegisterMiddleware(openaiMessageConnector);
        #endregion Create_Agent

        #region Chat_With_Agent
        var reply = await agent.SendAsync("Tell me a joke");
        Console.WriteLine($"Total token count: {totalTokenCount}");
        #endregion Chat_With_Agent

        #region verify_reply
        reply.Should().BeOfType<TextMessage>();
        totalTokenCount.Should().BeGreaterThan(0);
        #endregion verify_reply
    }

    public static async Task RunRagTaskAsync()
    {
        #region Create_Agent
        var apiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? throw new InvalidOperationException("Please set the environment variable OPENAI_API_KEY");
        var model = "gpt-3.5-turbo";
        var openaiClient = new OpenAIClient(apiKey);
        var openaiMessageConnector = new OpenAIChatRequestMessageConnector();
        var agent = new OpenAIChatAgent(
            openAIClient: openaiClient,
            name: "agent",
            modelName: model,
            systemMessage: "You are a helpful AI assistant")
            .RegisterMessageConnector()
            .RegisterMiddleware(async (messages, option, innerAgent, ct) =>
            {
                var today = DateTime.UtcNow;
                var todayMessage = new TextMessage(Role.System, $"Today is {today:yyyy-MM-dd}");
                messages = messages.Concat(new[] { todayMessage });
                return await innerAgent.GenerateReplyAsync(messages, option, ct);
            })
            .RegisterPrintMessage();
        #endregion Create_Agent

        #region Chat_With_Agent
        var reply = await agent.SendAsync("what's the date today");
        #endregion Chat_With_Agent
    }
}
