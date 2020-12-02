register_feed = """
    mutation RegisterFeed($url: String!) {
        registerFeed(url: $url) {
            feed {
                uuid
            }
        }
    }
"""

update_feed = """
    mutation UpdateFeed($uuid: UUID!) {
        updateFeed(uuid: $uuid) {
            success
        }
    }
"""

delete_feed = """
    mutation DeleteFeed($uuid: UUID!) {
        deleteFeed(uuid: $uuid) {
            success
        }
    }
"""

feed_update_state = """
    mutation FeedUpdateState($uuid: UUID!) {
        updateState(uuid: $uuid)
    }
"""

follow_feed = """
    mutation FollowFeed($uuid: UUID!) {
        followFeed(uuid: $uuid) {
            success
        }
    }
"""

unfollow_feed = """
    mutation UnFollowFeed($uuid: UUID!) {
        unFollowFeed(uuid: $uuid) {
            success
        }
    }
"""

read_item = """
    mutation ReadItem($uuid: UUID!) {
        readFeedItem(uuid: $uuid) {
            success
        }
    }
"""

unread_item = """
    mutation UnReadItem($uuid: UUID!) {
        unReadFeedItem(uuid: $uuid) {
            success
        }
    }
"""

feed_query = """
    query Feeds($orderBy: String!) {
        feeds(orderBy: $orderBy) {
        edges {
      node {
        uuid
        user{
          username
        }
        title
        subtitle
        rights
        url
        lastUpdated
        info
        language
            }
        }
    }
}
"""

feed_item_query = """
    query FeedItems($orderBy: String!) {
        feedItems(orderBy: $orderBy) {
        edges {
      node {
        uuid
        title
        dateModified
        content
        feed {
          uuid
          url
          title
          lastUpdated
        }
        }
        }
    }
}
"""
