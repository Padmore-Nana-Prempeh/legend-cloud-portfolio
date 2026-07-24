# MERIT Milestone 3 — Authentication and Edge Verification

## Status

**Milestone 3: Complete**

This milestone establishes the authenticated web entry point and secure edge layer for MERIT.

## Implemented Components

- Amazon Cognito User Pool for user authentication
- Cognito web application client without a client secret
- Email-based account verification
- Password recovery and reset workflow
- Amazon API Gateway REST API
- Cognito authorizer protecting authenticated API routes
- Amazon CloudFront distribution
- Private Amazon S3 frontend origin using Origin Access Control (OAC)
- AWS WAF Web ACL attached to CloudFront
- CloudFront security response headers
- CloudFront Function for static-export route rewriting
- Next.js static frontend
- AWS Amplify authentication integration
- Protected dashboard
- JWT-authenticated API test from the browser
- Restricted API CORS configuration

## Authentication Verification

The following user flows were verified successfully:

- User registration
- Cognito password policy enforcement
- Email verification
- Sign-in
- Sign-out
- Protected dashboard access
- Redirect of unauthenticated users to sign-in
- Forgot-password request
- Password reset using verification code
- Sign-in using the newly reset password
- JWT-authenticated request to the protected API

The protected production API request returned:

`HTTP 200`

## Edge and Security Verification

The following controls were verified:

- Direct access to the private frontend S3 origin returns `HTTP 403`
- CloudFront serves the application successfully
- AWS WAF is attached to the CloudFront distribution
- Managed WAF rules are enabled
- Rate-based protection is configured
- Security response headers are returned by CloudFront
- S3/KMS implementation details are not exposed through frontend response headers
- KMS permissions for CloudFront use the exact deployed distribution ARN
- The deployed KMS policy does not retain wildcard distribution scope
- API CORS is restricted to the deployed frontend origin

## Production Route Verification

The following production routes were verified through CloudFront and returned `HTTP 200`:

- `/`
- `/signin`
- `/register`
- `/confirm-signup`
- `/forgot-password`
- `/reset-password`
- `/dashboard`

A CloudFront viewer-request function rewrites clean application paths to the corresponding statically exported `index.html` files.

## Frontend Quality Verification

The frontend passed:

```text
npm run lint
0 errors
0 warnings
```

The production build also completed successfully with all MERIT authentication routes statically generated.

## Route 53 and Custom Domain Decision

The original architecture includes Route 53, ACM, and a custom HTTPS domain.

The development deployment currently uses the CloudFront-provided hostname because no project domain is owned yet.

Route 53, ACM custom-domain configuration, and the final branded hostname are therefore intentionally deferred to the publication/hardening milestone rather than creating unnecessary domain cost during development.

This is a deliberate implementation deviation, not an omitted security control.

## KMS OAC Policy Hardening

AWS CDK initially generates an OAC-related KMS policy using wildcard distribution scope to avoid a deployment-time circular dependency.

After the CloudFront distribution was created, MERIT was hardened by parameterizing the deployed distribution ARN and replacing the wildcard condition with an exact `StringEquals` condition.

The live KMS policy was verified after deployment.

## CORS Hardening

CORS was first discovered during authenticated browser testing when the protected API worked at the authorization layer but the browser rejected the request.

The API was subsequently configured with explicit CORS support and then hardened so that the allowed origin is supplied as a deployment parameter rather than using `*`.

Production browser testing confirmed that an authenticated request succeeds with `HTTP 200`.

## Dependency Audit Note

The frontend dependency audit currently reports three high-severity transitive dependency findings.

No forced dependency downgrade was applied because the proposed forced remediation would introduce inappropriate framework-version changes.

These findings are documented for controlled review during the final hardening/publication milestone.

## Repository Privacy Verification

Before preparing this milestone for commit:

- `.env.local` was confirmed ignored by Git
- Python virtual environments were confirmed ignored
- `node_modules`, `.next`, and static build output are excluded
- AI-agent helper files are excluded from the public frontend repository
- A source-level scan found no AWS access keys, secret-access-key strings, private keys, personal Gmail addresses, or University at Albany email addresses

No screenshots containing personal email addresses or verification codes are included in the public repository.

## Milestone Result

Milestone 3 provides a working production authentication and edge foundation for MERIT:

```text
User
  ↓
CloudFront + WAF
  ↓
Next.js frontend
  ↓
Amazon Cognito
  ↓
JWT
  ↓
API Gateway Cognito Authorizer
  ↓
Protected MERIT API
```

This establishes the secure authenticated boundary required before Milestone 4 introduces secure document upload.
