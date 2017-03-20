0.8
---
- Add cut_and_strip
- Add encode_object, define_decode_object
- Add schedule_shell_callback, schedule_curl_callback
- Add define_get_numbers
- Add format_decimal, format_number

0.7
---
- Add configuration.load_settings and configuration.save_settings
- Add disk.TemporaryFolder and disk.TemporaryPath
- Add math.divide_safely
- Remove parse_date_safely thanks to latest dateutil
- Replace get_interpretation_by_name with parse_settings

0.6
---
- Add iterable.flatten_dictionaries, iterable.merge_dictionaries
- Add log.format_summary, log.print_error
- Add table.normalize_key
- Filter keys in parse_nested_dictionary with is_key
- Make disk.compress and disk.uncompress compatible with non-Linux

0.5
---
- Add disk.make_enumerated_folder_for, disk.change_owner_and_group_recursively
- Add repository.get_github_repository_commit_timestamp
- Move queue.* to invisibleroads-sockets package
- Move repository.* to invisibleroads-repositories package

0.4
---
- Add disk.make_enumerated_folder
- Add log.parse_nested_dictionary

0.3
---
- Add queue.Pusher, queue.Puller, queue.Publisher, queue.Subscriber
- Add repository.download_github_repository, repository.get_github_ssh_url

0.2
---
- Add log.format_path
- Add text.remove_punctuation

0.1
---
- Add disk.compress, disk.uncompress
- Add text.compact_whitespace
