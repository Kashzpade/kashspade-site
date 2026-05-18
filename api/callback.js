export default async function handler(req, res) {

  const code = req.query.code;

  const params = new URLSearchParams();
  params.append("client_id", process.env.DISCORD_CLIENT_ID);
  params.append("client_secret", process.env.DISCORD_CLIENT_SECRET);
  params.append("grant_type", "authorization_code");
  params.append("code", code);
  params.append("redirect_uri", "https://ns-spade.vercel.app/api/callback");

  /* GET TOKEN */
  const tokenRes = await fetch("https://discord.com/api/oauth2/token", {
    method: "POST",
    body: params,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  });

  const token = await tokenRes.json();

  /* GET USER */
  const userRes = await fetch("https://discord.com/api/users/@me", {
    headers: {
      Authorization: `Bearer ${token.access_token}`
    }
  });

  const user = await userRes.json();

  /* SEND BACK TO FRONTEND */
  return res.send(`
    <script>
      localStorage.setItem("discordUser", JSON.stringify(${JSON.stringify(user)}));
      window.location.href = "/";
    </script>
  `);
}