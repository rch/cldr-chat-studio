/*******************************************************************************
 * CLOUDERA APPLIED MACHINE LEARNING PROTOTYPE (AMP)
 * (C) Cloudera, Inc. 2024
 * All rights reserved.
 *
 * Applicable Open Source License: Apache 2.0
 *
 * NOTE: Cloudera open source products are modular software products
 * made up of hundreds of individual components, each of which was
 * individually copyrighted.  Each Cloudera open source product is a
 * collective work under U.S. Copyright Law. Your license to use the
 * collective work is as provided in your written agreement with
 * Cloudera.  Used apart from the collective work, this file is
 * licensed for your use pursuant to the open source license
 * identified above.
 *
 * This code is provided to you pursuant a written agreement with
 * (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
 * this code. If you do not have a written agreement with Cloudera nor
 * with an authorized and properly licensed third party, you do not
 * have any rights to access nor to use this code.
 *
 * Absent a written agreement with Cloudera, Inc. ("Cloudera") to the
 * contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
 * KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
 * WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
 * IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
 * FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
 * AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
 * ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
 * OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
 * DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
 * CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
 * RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
 * BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
 * DATA.
 ******************************************************************************/

import { Button, Flex, Image, Typography } from "antd";
import { cdlGray050 } from "src/cuix/variables.ts";
import { useNavigate } from "@tanstack/react-router";
import GettingStartedSellingPoints from "src/components/SellingPoints/GettingStartedSellingPoints.tsx";
import Images from "src/components/images/Images.ts";

const Splash = () => {
  return (
    <Flex
      flex={1}
      style={{
        padding: 64,
        paddingTop: 135,
        paddingLeft: 12,
        backgroundColor: cdlGray050,
      }}
      justify="center"
    >
      <img src={Images.Welcome} alt="welcome" style={{ height: 535 }} />
    </Flex>
  );
};

const GettingStarted = () => {
  const navigate = useNavigate();
  return (
    <Flex style={{ height: "100vh" }}>
      <Flex style={{ padding: 64 }} flex={1} vertical>
        <Image
          src={Images.Cloudera}
          alt="cloudera"
          style={{ width: 125 }}
          preview={false}
        />
        <Flex vertical gap={24}>
          <Typography.Title
            style={{
              fontSize: 64,
              marginTop: 133,
              marginBottom: 0,
              paddingBottom: 0,
              paddingTop: 0,
            }}
          >
            RAG Studio
          </Typography.Title>
          <Typography.Text>Private AI chats at your fingertips</Typography.Text>
          <GettingStartedSellingPoints />
          <Button
            type="primary"
            size="large"
            style={{ width: 113 }}
            onClick={() => {
              navigate({ to: "/chats" }).catch(() => null);
            }}
          >
            Get Started
          </Button>
        </Flex>
      </Flex>
      <Splash />
    </Flex>
  );
};

export default GettingStarted;
