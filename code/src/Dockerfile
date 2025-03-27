FROM php:8.1-apache

# Install dependencies
RUN apt-get update && apt-get install -y \
    libzip-dev \
    zip \
    unzip \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libldap2-dev \
    wget \
    zlib1g-dev \
    libicu-dev \
    libsodium-dev \
    libxml2-dev \
    libbz2-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-configure intl \
    && docker-php-ext-install -j$(nproc) \
        gd \
        mysqli \
        pdo \
        pdo_mysql \
        ldap \
        zip \
        intl \
        sodium \
        exif \
        opcache \
        bz2

# Configure PHP
RUN echo "session.cookie_httponly = On" >> /usr/local/etc/php/php.ini

# Configure Apache
RUN a2enmod rewrite
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/html/glpi\n\
    <Directory /var/www/html/glpi>\n\
        Options Indexes FollowSymLinks\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Download and install GLPI
RUN wget https://github.com/glpi-project/glpi/releases/download/10.0.10/glpi-10.0.10.tgz \
    && tar xvf glpi-10.0.10.tgz -C /var/www/html/ \
    && rm glpi-10.0.10.tgz \
    && chown -R www-data:www-data /var/www/html/glpi \
    && chmod -R 755 /var/www/html/glpi

# Set proper permissions for specific directories
RUN chmod -R 777 /var/www/html/glpi/files \
    && chmod -R 777 /var/www/html/glpi/config \
    && chmod -R 777 /var/www/html/glpi/marketplace

WORKDIR /var/www/html/glpi
