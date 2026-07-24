import { Amplify } from "aws-amplify";

const region = process.env.NEXT_PUBLIC_AWS_REGION;
const userPoolId = process.env.NEXT_PUBLIC_COGNITO_USER_POOL_ID;
const userPoolClientId =
  process.env.NEXT_PUBLIC_COGNITO_USER_POOL_CLIENT_ID;

if (!region || !userPoolId || !userPoolClientId) {
  throw new Error("Missing MERIT Cognito environment configuration.");
}

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId,
      userPoolClientId,
    },
  },
});

export { Amplify };