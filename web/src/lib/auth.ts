import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import { SignJWT } from "jose";

const jwtSecret = new TextEncoder().encode(process.env.NEXTAUTH_SECRET);

export const { handlers, signIn, signOut, auth } = NextAuth({
  trustHost: true,
  providers: [
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  session: { strategy: "jwt" },
  callbacks: {
    authorized({ auth }) {
      return !!auth?.user;
    },
    async jwt({ token, account }) {
      // Pin sub to the OAuth provider's stable ID so it survives logout/login.
      // NextAuth v5 beta sets sub to a random UUID without a DB adapter.
      if (account) {
        token.sub = `${account.provider}:${account.providerAccountId}`;
      }
      if ((account || !token.backendToken) && token.sub) {
        token.backendToken = await new SignJWT({
          sub: token.sub,
          email: token.email,
          name: token.name,
        })
          .setProtectedHeader({ alg: "HS256" })
          .setExpirationTime("30d")
          .sign(jwtSecret);
      }
      return token;
    },
    async session({ session, token }) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      (session as any).accessToken = token.backendToken;
      if (token.sub) session.user.id = token.sub;
      return session;
    },
  },
  pages: {
    signIn: "/login",
    error: "/login",
  },
});
