FROM ruby:3.3-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    # For jekyll_picture_tag gem
    libvips-dev libpng-dev libjpeg-dev imagemagick \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /site

# Run `bundle update` to add/update gems
RUN gem update --system && gem install bundler jekyll && gem cleanup

COPY Gemfile Gemfile.lock ./

RUN bundle install --no-cache

ENTRYPOINT ["sleep", "infinity"]
