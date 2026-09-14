=====
Types
=====

All pydantic models representing Rubika Bot API objects. They all
inherit from :class:`~aiorubi.types.base.RubikaObject`.

Base
====

.. autoclass:: aiorubi.types.base.RubikaObject
   :members:

Update types
============

.. autoclass:: aiorubi.types.update.Update
   :members:

.. autoclass:: aiorubi.types.message.Message
   :members:

.. autoclass:: aiorubi.types.inline_message.InlineMessage
   :members:

.. autoclass:: aiorubi.types.removed_message.RemovedMessage
   :members:

.. autoclass:: aiorubi.types.started_bot.StartedBot
   :members:

.. autoclass:: aiorubi.types.stopped_bot.StoppedBot
   :members:

.. autoclass:: aiorubi.types.message_id.MessageID
   :members:

Content
=======

.. autoclass:: aiorubi.types.file.File
   :members:

.. autoclass:: aiorubi.types.sticker.Sticker
   :members:

.. autoclass:: aiorubi.types.location.Location
   :members:

.. autoclass:: aiorubi.types.contact_message.ContactMessage
   :members:

.. autoclass:: aiorubi.types.poll.Poll
   :members:

.. autoclass:: aiorubi.types.poll_status.PollStatus
   :members:

.. autoclass:: aiorubi.types.forwarded_from.ForwardedFrom
   :members:

.. autoclass:: aiorubi.types.forwarded_no_link.ForwardedNoLink
   :members:

.. autoclass:: aiorubi.types.aux_data.AuxData
   :members:

.. autoclass:: aiorubi.types.metadata.MetaData
   :members:

.. autoclass:: aiorubi.types.metadata.MetaDataPart
   :members:

.. autoclass:: aiorubi.types.custom.DateTime
   :members:

Keypads and buttons
===================

.. autoclass:: aiorubi.types.keypad.Keypad
   :members:

.. autoclass:: aiorubi.types.keypad_row.KeypadRow
   :members:

.. autoclass:: aiorubi.types.button.Button
   :members:

.. autoclass:: aiorubi.types.button_selection.ButtonSelection
   :members:

.. autoclass:: aiorubi.types.button_selection_item.ButtonSelectionItem
   :members:

.. autoclass:: aiorubi.types.button_calendar.ButtonCalendar
   :members:

.. autoclass:: aiorubi.types.button_number_picker.ButtonNumberPicker
   :members:

.. autoclass:: aiorubi.types.button_string_picker.ButtonStringPicker
   :members:

.. autoclass:: aiorubi.types.button_textbox.ButtonTextbox
   :members:

.. autoclass:: aiorubi.types.button_location.ButtonLocation
   :members:

Bot & chat
==========

.. autoclass:: aiorubi.types.bot_info.BotInfo
   :members:

.. autoclass:: aiorubi.types.bot_command.BotCommand
   :members:

.. autoclass:: aiorubi.types.chat.Chat
   :members:

Files transfer
==============

.. autoclass:: aiorubi.types.input_file.InputFile
   :members:

.. autoclass:: aiorubi.types.downloadable.Downloadable
   :members:

.. autoclass:: aiorubi.types.download_url.DownloadUrl
   :members:

.. autoclass:: aiorubi.types.upload_url.UploadUrl
   :members:

.. autoclass:: aiorubi.types.get_updates_response.GetUpdatesResponse
   :members:

.. autoclass:: aiorubi.types.update_endpoint_status.UpdateEndpointsStatus
   :members:

Misc
====

.. autoclass:: aiorubi.types.error_event.ErrorEvent
   :members:

.. autoclass:: aiorubi.types.response_parameters.ResponseParameters
   :members:

.. autoclass:: aiorubi.types.message_keypad_update.MessageKeypadUpdate
   :members:

.. autoclass:: aiorubi.types.message_text_update.MessageTextUpdate
   :members:
