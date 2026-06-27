# Deploy Landing Page to ethiovibe.com.et

The Plesk server blocks programmatic uploads (FTP closed, SSH needs key auth,
file manager API rejects non-browser clients). Upload manually — takes 60 seconds.

## Steps

1. Open **https://lin3.ethiotelecom.et:8443** in your browser
2. Login: `ethiovib` / `Emamia@Ababia@0913278186`
3. Click **File Manager** in the left sidebar
4. Click **httpdocs** folder
5. Click **Upload File** button (top toolbar)
6. Drag or browse to: `website/index.html`
7. Done! Visit **https://ethiovibe.com.et** to see your site

## What gets deployed

One file: `index.html` — self-contained, no dependencies, works offline.
