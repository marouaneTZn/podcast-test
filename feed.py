import yaml
import xml.etree.ElementTree as xml_tree

# Define link_prefix
link_prefix = 'http://example.com/'  # Change this to your actual base URL

# Load YAML data
with open('feed.yaml', 'r') as file:
    yaml_data = yaml.safe_load(file)

# Register namespaces for itunes and content
xml_tree.register_namespace('itunes', 'https://www.itunes.com/dtds/podcast-1.0.dtd')
xml_tree.register_namespace('content', 'http://purl.org/rss/1.0/modules/content/')

# Create RSS structure
rss_element = xml_tree.Element('rss', {
    'version': '2.0',
    'xmlns:itunes': 'https://www.itunes.com/dtds/podcast-1.0.dtd',
    'xmlns:content': 'http://purl.org/rss/1.0/modules/content/'
})

channel_element = xml_tree.SubElement(rss_element, 'channel')

# Populate channel metadata
xml_tree.SubElement(channel_element, 'title').text = yaml_data.get('title', 'No Title')
xml_tree.SubElement(channel_element, 'format').text = yaml_data.get('format', 'N/A')
xml_tree.SubElement(channel_element, 'subtitle').text = yaml_data.get('subtitle', 'No Subtitle')
xml_tree.SubElement(channel_element, 'itunes:author').text = yaml_data.get('author', 'Unknown Author')
xml_tree.SubElement(channel_element, 'description').text = yaml_data.get('description', 'No Description')
xml_tree.SubElement(channel_element, 'itunes:image', {'href': link_prefix + yaml_data.get('image', 'default.jpg')})
xml_tree.SubElement(channel_element, 'language').text = yaml_data.get('language', 'en')
xml_tree.SubElement(channel_element, 'link').text = link_prefix

category = yaml_data.get('category', 'Uncategorized')
xml_tree.SubElement(channel_element, 'itunes:category', {'text': category})

# Populate items
for item in yaml_data.get('items', []):
    item_element = xml_tree.SubElement(channel_element, 'item')
    xml_tree.SubElement(item_element, 'title').text = item.get('title', 'No Title')
    xml_tree.SubElement(item_element, 'itunes:author').text = yaml_data.get('author', 'Unknown Author')
    xml_tree.SubElement(item_element, 'description').text = item.get('description', 'No Description')
    xml_tree.SubElement(item_element, 'itunes:duration').text = item.get('duration', '0:00')
    xml_tree.SubElement(item_element, 'pubDate').text = item.get('published', 'Unknown Date')

    # Handle enclosure attributes
    file_url = link_prefix + item.get('file', 'default.mp3')
    file_length = item.get('length', '0')
    xml_tree.SubElement(item_element, 'enclosure', {
        'url': file_url,
        'type': 'audio/mpeg',
        'length': file_length
    })

# Write to XML file
output_tree = xml_tree.ElementTree(rss_element)
output_tree.write('podcast.xml', encoding='UTF-8', xml_declaration=True)
