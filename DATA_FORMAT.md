# DATA FORMAT

## Identifier

Each GeoJSON feature has an `id` field. The ID is a hash based on the `ref` and `@spider` fields and should be consistent between builds. You might use this to determine if new objects show up or disappear between builds.

## Geometry

In most cases, the feature will include a `geometry` field following [the GeoJSON spec](https://tools.ietf.org/html/rfc7946#section-3.1). There are some spiders that aren't able to recover a position from the venue's website. In those cases, the geometry is set to `null` and only the properties are included.

Although it's not supported at the time of this writing, we hope to include a geocoding step in the pipeline so that these feature will get a position added.

## Properties

Each GeoJSON feature will have a `properties` object with the following keys:

| Name | Required? | Description |
|---|---|---|
| `ref`           | Yes | A unique identifier for this feature inside this spider. The code that generates the output will remove duplicates based on the value of this key. 
| `chain_id`      | Yes | Static attribute. Read more here [Place s  category system](https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics-places/places-chain-system-full.html)
| `chain_name`    | Yes | Static attribute. Read more here [Place s  category system](https://developer.here.com/documentation/geocoding-search-api/dev_guide/topics-places/places-chain-system-full.html)
| `addr_full`     | No  | Usually this follows the format of street, city, province, postcode address. This field might exist instead of the other address-related fields, especially if the spider can't reliably extract the individual parts of the address.
| `housenumber`   | No  | The house number part of the address.
| `street`        | No  | The street name.
| `city`          | No  | The city part of the address.
| `state`         | No  | The state or province part of the address.
| `postcode`      | No  | The postcode part of the address.
| `country`       | No  | The country part of the address.
| `phone`         | No  | The telephone number for the venue. Note that this is usually pulled from a website assuming local visitors, so it probably doesn't include the country code.
| `website`       | No  | Static URL of the website from which you collect data. Example https://www.mcdonalds.rs/
| `store_url`     | No  | Dynamic URL of the page on the website. Usually we add this attribute when website renders information about different places on a different pages.
| `opening_hours` | No  | [OpenStreetMap's `opening_hours` format](https://wiki.openstreetmap.org/wiki/Key:opening_hours#Examples).
| `lat`           | No  | Latitude
| `lon`           | No  | Longitude