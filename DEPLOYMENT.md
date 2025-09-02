# Floodlight - DigitalOcean Deployment Guide

This guide explains how to deploy Floodlight on DigitalOcean App Platform.

## Prerequisites

1. GitHub repository: `https://github.com/codeforpakistan/floodlight`
2. DigitalOcean account
3. Domain configured (floods.pk)

## Deployment Steps

### 1. Create App on DigitalOcean

1. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Choose "GitHub" as source
4. Select repository: `codeforpakistan/floodlight`
5. Branch: `master`

### 2. Configure App Settings

Use the provided `.do/app.yaml` specification or configure manually:

**App Info:**
- Name: `floodlight`
- Region: Choose closest to your users

**Service Configuration:**
- Service Type: Web Service
- Source Directory: `/` (root)
- Run Command: `gunicorn project.wsgi:application --bind 0.0.0.0:$PORT`
- HTTP Port: 8080
- Instance Size: Basic ($5/month)

### 3. Environment Variables

Set these in DigitalOcean App Platform:

```bash
DEBUG=False
DJANGO_SETTINGS_MODULE=project.production_settings
SECRET_KEY=your-very-secure-secret-key-here
ALLOWED_HOSTS=.ondigitalocean.app,floods.pk,www.floods.pk
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@floods.pk
DJANGO_SUPERUSER_PASSWORD=secure-admin-password
```

### 4. Database Configuration

1. Add PostgreSQL database to your app
2. DigitalOcean will automatically set `DATABASE_URL`
3. Database name: `floodlight-db`

### 5. Domain Setup

1. In DigitalOcean App settings, add custom domains:
   - `floods.pk` (primary)
   - `www.floods.pk` (alias)
2. Update DNS records at your domain registrar:
   - Add CNAME record: `floods.pk` → `your-app-name.ondigitalocean.app`
   - Add CNAME record: `www.floods.pk` → `your-app-name.ondigitalocean.app`

### 6. Post-Deployment Setup

After first deployment, run these commands via the console:

```bash
# Create superuser and load initial data
python manage.py production_setup --create-superuser --seed-data

# Or run individually:
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py seed_data
```

## Files Added for Deployment

- `.do/app.yaml` - DigitalOcean App Platform specification
- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration
- `project/production_settings.py` - Production Django settings
- `.env.example` - Environment variables template
- `app/management/commands/production_setup.py` - Production setup command

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `False` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DATABASE_URL` | Database connection | Auto-set by DigitalOcean |
| `ALLOWED_HOSTS` | Allowed host names | `.ondigitalocean.app,floods.pk` |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | `admin` |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | `admin@floods.pk` |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | `secure-password` |

## Security Considerations

1. **Secret Key**: Generate a new secret key for production
2. **Database**: Use strong database passwords
3. **Admin Account**: Use strong admin credentials
4. **HTTPS**: DigitalOcean provides SSL certificates automatically
5. **Environment Variables**: Never commit sensitive data to version control

## Monitoring & Logs

- View application logs in DigitalOcean Apps console
- Monitor resource usage and performance metrics
- Set up alerts for downtime or errors

## Scaling

- Start with Basic ($5/month) instance
- Scale up to Professional ($12/month) for higher traffic
- Add more instances for horizontal scaling

## Troubleshooting

1. **Build Failures**: Check build logs for dependency issues
2. **Database Issues**: Verify DATABASE_URL is set correctly
3. **Static Files**: Ensure `collectstatic` runs during deployment
4. **Domain Issues**: Verify DNS records and SSL certificates

## Support

For deployment issues:
1. Check DigitalOcean documentation
2. Review application logs
3. Contact Code for Pakistan team

---

**Production URL**: https://floods.pk
**Admin Panel**: https://floods.pk/admin
**Repository**: https://github.com/codeforpakistan/floodlight
