﻿// Copyright (c) 2023 - 2024, Owners of https://github.com/ag2ai
// SPDX-License-Identifier: Apache-2.0
// Contributions to this project, i.e., https://github.com/ag2ai/ag2, 
// are licensed under the Apache License, Version 2.0 (Apache-2.0).
// Portions derived from  https://github.com/microsoft/autogen under the MIT License.
// SPDX-License-Identifier: MIT
// Copyright (c) Microsoft Corporation. All rights reserved.
// RoundRobinGroupChat.cs

using System;
using System.Collections.Generic;

namespace AutoGen.Core;

/// <summary>
/// Obsolete: please use <see cref="RoundRobinGroupChat"/>
/// </summary>
[Obsolete("please use RoundRobinGroupChat")]
public class SequentialGroupChat : RoundRobinGroupChat
{
    [Obsolete("please use RoundRobinGroupChat")]
    public SequentialGroupChat(IEnumerable<IAgent> agents, List<IMessage>? initializeMessages = null)
        : base(agents, initializeMessages)
    {
    }
}

/// <summary>
/// A group chat that allows agents to talk in a round-robin manner.
/// </summary>
public class RoundRobinGroupChat : GroupChat
{
    public RoundRobinGroupChat(
        IEnumerable<IAgent> agents,
        List<IMessage>? initializeMessages = null)
        : base(agents, initializeMessages: initializeMessages)
    {
    }
}
