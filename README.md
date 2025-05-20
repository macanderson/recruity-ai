# AGENTS.md

## Monorepo Overview

- **Structure**:

  - `apps/api`: Python-based FastAPI application handling API requests and authentication.
  - `apps/web`: Next.js frontend application.
  - `apps/docs`: Next.js documentation site utilizing `.mdx` files for content rendering.
  - `apps/tasks`: Python application for scheduled tasks using APScheduler and Redis.
  - `packages/ui-components`: Shared UI components using shadcn/ui.
  - `packages/config/eslint-config`: Centralized ESLint configurations.
  - `packages/config/typescript-config`: Centralized TypeScript configurations.
  - `packages/prisma`: Prisma schema and generated clients.([Class Central][1])

- **Routing**:

  - All frontend requests are routed through the `apps/api` application.

- **Database**:

  - PostgreSQL managed via Supabase.
  - Multi-tenancy is enabled from the outset.

### Utilities

This Turborepo has some additional tools already setup for you:

- [TypeScript](https://www.typescriptlang.org/) for static type checking
- [ESLint](https://eslint.org/) for code linting
- [Prettier](https://prettier.io) for code formatting

### Build

To build all apps and packages, run the following command:

```
cd recruity-ai
pnpm build
```

### Develop

To develop all apps and packages, run the following command:

```
cd recruity-ai
pnpm dev
```

### Remote Caching

> [!TIP]
> Vercel Remote Cache is free for all plans. Get started today at [vercel.com](https://vercel.com/signup?/signup?utm_source=remote-cache-sdk&utm_campaign=free_remote_cache).

Turborepo can use a technique known as [Remote Caching](https://turborepo.com/docs/core-concepts/remote-caching) to share cache artifacts across machines, enabling you to share build caches with your team and CI/CD pipelines.

By default, Turborepo will cache locally. To enable Remote Caching you will need an account with Vercel. If you don't have an account you can [create one](https://vercel.com/signup?utm_source=turborepo-examples), then enter the following commands:

```
cd recruity-ai
npx turbo login
```

This will authenticate the Turborepo CLI with your [Vercel account](https://vercel.com/docs/concepts/personal-accounts/overview).

Next, you can link your Turborepo to your Remote Cache by running the following command from the root of your Turborepo:

```
npx turbo link
```

## Useful Links

Learn more about the power of Turborepo:

- [Tasks](https://turborepo.com/docs/crafting-your-repository/running-tasks)
- [Caching](https://turborepo.com/docs/crafting-your-repository/caching)
- [Remote Caching](https://turborepo.com/docs/core-concepts/remote-caching)
- [Filtering](https://turborepo.com/docs/crafting-your-repository/running-tasks#using-filters)
- [Configuration Options](https://turborepo.com/docs/reference/configuration)
- [CLI Usage](https://turborepo.com/docs/reference/command-line-reference)

## Authentication Architecture

### Frontend: Next.js with Auth.js (NextAuth.js)

- **Library**: Utilize [Auth.js](https://authjs.dev/), formerly NextAuth.js, for authentication in `apps/web` and `apps/docs`.
- **Credentials Provider**: Implement a custom credentials provider to handle email and password authentication.&#x20;
- **Session Management**: Configure session handling using JWTs to maintain stateless sessions across your applications.

### Backend: FastAPI with JWT

- **Authentication**: Employ FastAPI's OAuth2PasswordBearer for secure authentication flows.&#x20;
- **JWT Handling**: Use `PyJWT` to encode and decode JWTs, ensuring secure token-based authentication.
- **Password Hashing**: Implement `passlib` for hashing and verifying user passwords securely.
- **Email Verification & Password Reset**:

  - **Token Generation**: Generate time-limited JWTs for email verification and password reset processes.
  - **Endpoints**:

    - `POST /auth/register`: Handles user registration and sends verification emails.
    - `POST /auth/login`: Manages user login and JWT issuance.
    - `POST /auth/verify-email`: Processes email verification tokens.
    - `POST /auth/request-password-reset`: Initiates password reset by sending a reset link.
    - `POST /auth/reset-password`: Completes the password reset process.

## Email Verification & Password Reset

- **Email Service**: Integrate [Mailgun](https://www.mailgun.com/) for sending transactional emails, including verification and password reset emails. Mailgun offers a developer-friendly API and reliable delivery.
- **Email Verification**:

  - Upon user registration, send a verification email containing a unique JWT token.
  - The token should have a short expiration time (e.g., 24 hours) to enhance security.
  - Upon clicking the verification link, the backend validates the token and activates the user's account.

- **Password Reset**:

  - Allow users to request a password reset by providing their registered email.
  - Send a password reset email containing a unique JWT token.
  - Upon clicking the reset link, the backend validates the token and allows the user to set a new password.([FastAPI][2])

## Prisma ORM

Use a ts configuration file to point the prisma cli to the correct location for the prisma schema.

```typescript
import path from "node:path";
import { defineConfig } from "prisma/config";

export default defineConfig({
  earlyAccess: true,
  schema: path.join("packages", "prisma", "schema.prisma"),
});
```

- **Schema Location**:

  - The Prisma schema is located at `packages/prisma/schema.prisma`.

- **Schema Generators**:

  - setup the client generator for python
  - generate typescript types only
  - setup the erd generator

- **Naming Conventions**:

  - **Models**:

    - Use singular PascalCase for model names (e.g., `User`).
    - Map to plural snake_case table names using `@@map` (e.g., `@@map("users")`).

  - **Fields**:

    - Use camelCase for field names (e.g., `createdAt`).
    - Map to snake_case column names using `@map` (e.g., `@map("created_at")`).

- **Client Generation**:

  - Run `pnpm prisma generate` to generate clients.
  - Python types for the API are generated using [prisma-client-py](https://github.com/RobertCraigie/prisma-client-py).
  - TypeScript stubs are generated for Next.js applications; CRUD operations are not included on the frontend.

## System Audit Fields

Include the following audit fields in all Prisma models:

- `createdAt`: `DateTime` with `@default(now())`, mapped to `created_at`.
- `updatedAt`: `DateTime` with `@updatedAt`, mapped to `updated_at`.
- `deletedAt`: Optional `DateTime`, mapped to `deleted_at`.
- `createdById`: `String` referencing the `User` model, mapped to `created_by_id`.
- `updatedById`: `String` referencing the `User` model, mapped to `updated_by_id`.
- `deletedById`: Optional `String` referencing the `User` model, mapped to `deleted_by_id`.

Example:

```prisma
model ExampleModel {
  id           String   @id @default(cuid())
  createdAt    DateTime @default(now()) @map("created_at")
  updatedAt    DateTime @updatedAt @map("updated_at")
  deletedAt    DateTime? @map("deleted_at")
  createdById  String   @map("created_by_id")
  updatedById  String   @map("updated_by_id")
  deletedById  String?  @map("deleted_by_id")

  createdBy    User     @relation("createdBy", fields: [createdById], references: [id])
  updatedBy    User     @relation("updatedBy", fields: [updatedById], references: [id])
  deletedBy    User?    @relation("deletedBy", fields: [deletedById], references: [id])

  @@map("example_models")
}
```

## Multi-Tenancy

- **Implementation**:

  - Each database table includes a `tenant_id` column.
  - Row-level security (RLS) policies are enforced in Supabase to ensure data isolation between tenants.

- **Best Practices**:

  - Always include `tenant_id` in queries to maintain data segregation.
  - Avoid hardcoding tenant identifiers; retrieve them from the authenticated user's context.

## Scheduled Tasks Application (`apps/tasks`)

- **Purpose**:

  - Handles scheduled and background tasks using APScheduler and Redis.

- **Dependencies**:

  - `APScheduler` for scheduling tasks.
  - `Redis` as the task queue backend.
  - `rq` (Redis Queue) for managing background job execution.

- **Setup**:

  - Ensure Redis server is running and accessible.
  - Configure APScheduler to use `RedisJobStore` for job persistence.
  - Define scheduled tasks within the application, specifying triggers and job functions.

- **Example Configuration**:

  ```python
  from apscheduler.schedulers.background import BackgroundScheduler
  from apscheduler.jobstores.redis import RedisJobStore
  from redis import Redis
  from rq import Queue

  # Initialize Redis connection
  redis_conn = Redis(host='localhost', port=6379, db=0)

  # Configure job stores
  jobstores = {
      'default': RedisJobStore(connection=redis_conn)
  }

  # Initialize scheduler
  scheduler = BackgroundScheduler(jobstores=jobstores)
  scheduler.start()

  # Initialize RQ queue
  task_queue = Queue(connection=redis_conn)

  # Define a sample task
  def sample_task():
      print("Executing scheduled task.")

  # Schedule the task
  scheduler.add_job(sample_task, 'interval', minutes=10)
  ```

- **Best Practices**:

  - Use unique job IDs to prevent conflicts.
  - Handle exceptions within scheduled tasks to prevent scheduler crashes.
  - Monitor task execution and failures using appropriate logging mechanisms.([TheCowBlog][3], [TestDriven.io][4])

## Documentation Site (`apps/docs`)

- **Purpose**:

  - Serves as the project's documentation site, built with Next.js and utilizing `.mdx` files for content rendering.

- **MDX Integration**:

  - The `apps/docs` application is configured to support `.mdx` files, allowing for the combination of Markdown and JSX for rich content creation.
  - This setup enables the embedding of React components within Markdown content, facilitating interactive and dynamic documentation pages.

- **Configuration**:

  - Ensure that the Next.js configuration (`next.config.js` or `next.config.mjs`) includes support for `.mdx` files.
  - Set up the necessary MDX components and plugins as required for the documentation site's needs.

- **Best Practices**:

  - Organize documentation content logically within the \`apps/docs

